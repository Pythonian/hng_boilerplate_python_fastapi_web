from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from api.v1.models.blog import Blog
from api.db.database import get_db
from api.utils.json_response import JsonResponseDict

blog = APIRouter(prefix="/blogs", tags=["Blog"])


@blog.get("", status_code=status.HTTP_200_OK)
def list_blog(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    try:
        offset = (page - 1) * page_size
        query = (
            db.query(Blog)
            .filter(Blog.is_deleted == False)
            .order_by(Blog.created_at.desc())
        )
        total_count = query.count()
        blogs = query.offset(offset).limit(page_size).all()

        next_page = None
        if offset + page_size < total_count:
            next_page = f"/api/v1/blogs?page={page + 1}&page_size={page_size}"

        prev_page = None
        if page > 1:
            prev_page = f"/api/v1/blogs?page={page - 1}&page_size={page_size}"

        results = []
        for blog in blogs:
            blog_dict = {
                "id": blog.id,
                "title": blog.title,
                "excerpt": blog.excerpt,
                "image_url": blog.image_url,
                "tags": blog.tags,
                "created_at": blog.created_at,
            }
            results.append(blog_dict)

        return JsonResponseDict(
            message="Blog Posts fetched successfully",
            data={
                "count": total_count,
                "next": next_page,
                "previous": prev_page,
                "results": results,
            },
            status_code=status.HTTP_200_OK,
        )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )