from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ForbiddenError, ParamError
from app.repositories.share_repo import ShareRepo
from app.repositories.voice_repo import VoiceRepo
from app.schemas.share import SharedVoiceVO
from app.schemas.voice import VoiceVO


class ShareService:
    def __init__(self, db: Session):
        self.repo = ShareRepo(db)
        self.voice_repo = VoiceRepo(db)

    def share_voice(self, voice_id: int, user_id: int, tags: str | None = None) -> SharedVoiceVO:
        voice = self.voice_repo.get_by_id(voice_id)
        if not voice:
            raise NotFoundError("音色")
        if voice.user_id != user_id:
            raise ForbiddenError()
        if voice.status != 1:
            raise ParamError("音色正在训练中，无法分享")
        existing = self.repo.get_share_by_voice(voice_id)
        if existing:
            raise ParamError("该音色已分享")

        share = self.repo.create_share(voice_id=voice_id, user_id=user_id, tags=tags)
        return SharedVoiceVO(
            share_id=share.share_id,
            voice_id=voice.voice_id,
            voice_name=voice.voice_name,
            user_id=user_id,
            download_count=0,
            tags=tags,
            sample_url=voice.sample_url,
            created_at=share.created_at,
        )

    def unshare_voice(self, voice_id: int, user_id: int):
        share = self.repo.get_share_by_voice(voice_id)
        if not share:
            raise NotFoundError("分享记录")
        if share.user_id != user_id:
            raise ForbiddenError()
        self.repo.update_status(share.share_id, 0)

    def list_public(self, keyword: str | None, page: int, page_size: int) -> tuple[list[SharedVoiceVO], int]:
        items, total = self.repo.list_public(keyword, page, page_size)
        result = []
        for s in items:
            result.append(
                SharedVoiceVO(
                    share_id=s.share_id,
                    voice_id=s.voice.voice_id,
                    voice_name=s.voice.voice_name,
                    user_id=s.user_id,
                    download_count=s.download_count,
                    tags=s.tags,
                    sample_url=s.voice.sample_url,
                    created_at=s.created_at,
                )
            )
        return result, total

    def download_voice(self, share_id: int, user_id: int) -> VoiceVO:
        share = self.repo.get_share_by_id(share_id)
        if not share or share.status != 1:
            raise NotFoundError("分享记录")

        original_voice = self.voice_repo.get_by_id(share.voice_id)
        if not original_voice:
            raise NotFoundError("音色")

        # create a copy in downloader's voice library
        new_voice = self.voice_repo.create(
            user_id=user_id,
            voice_name=original_voice.voice_name,
            clone_mode=original_voice.clone_mode,
        )
        new_voice.status = 1
        new_voice.source = "shared"
        new_voice.source_share_id = share_id
        new_voice.model_path = original_voice.model_path
        new_voice.sample_url = original_voice.sample_url

        self.repo.record_download(share_id, user_id, share.voice_id)
        return VoiceVO.model_validate(new_voice)

    def list_downloads(self, user_id: int, page: int, page_size: int) -> tuple[list[VoiceVO], int]:
        items, total = self.repo.get_downloads_by_user(user_id, page, page_size)
        voices = []
        for d in items:
            v = self.voice_repo.get_by_id(d.voice_id)
            if v:
                voices.append(VoiceVO.model_validate(v))
        return voices, total
