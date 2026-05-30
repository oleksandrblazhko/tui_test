import numpy as np

from models.tag import Tag
from models.tagged_object import TaggedObject


class TagManager:

    def __init__(
        self,
        num_tags,
        to_ids,
        to_offsets
    ):

        self.TAG_D = 150
        self.TO_D = 150

        self.tags = [
            Tag(i)
            for i in range(num_tags)
        ]

        self.tagged_objects = []

        self.active_tags = []

        self.active_tos = []

        for ids, offsets in zip(
            to_ids,
            to_offsets
        ):

            self.tagged_objects.append(
                TaggedObject(
                    ids,
                    offsets
                )
            )

    def set(
        self,
        tag_id,
        tx,
        ty,
        tz,
        rx,
        ry,
        rz,
        corners
    ):

        self.tags[tag_id].set(
            tx,
            ty,
            tz,
            rx,
            ry,
            rz,
            corners
        )

    def update(self):

        self.active_tags.clear()
        self.active_tos.clear()

        for tag in self.tags:

            tag.check_active()

            if tag.active:
                self.active_tags.append(tag.tag_id)

        from config import HOMOGRAPHY_READY

        if not HOMOGRAPHY_READY:
            return

        for tagged_object in self.tagged_objects:

            active_tags = []

            for tag_id in tagged_object.ids:

                if self.tags[tag_id].active:

                    active_tags.append(
                        self.tags[tag_id]
                    )

            if len(active_tags) > 0:

                self._update_tagged_object(
                    tagged_object,
                    active_tags
                )

            else:

                tagged_object.set_inactive()

        for index, obj in enumerate(
            self.tagged_objects
        ):

            if obj.active:
                self.active_tos.append(index)
                