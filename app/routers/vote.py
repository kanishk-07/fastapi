from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/votes",
    tags=['Votes']
)

@router.post("/create-vote", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    if vote.dir!=0 and vote.dir!=1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"vote data is invalid")
    post_query = db.query(models.Post).filter(models.Post.post_id==vote.post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==current_user.id)
    found_vote = vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Already liked")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"detail": "added vote"}
    elif vote.dir==0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"detail": "deleted vote"}
