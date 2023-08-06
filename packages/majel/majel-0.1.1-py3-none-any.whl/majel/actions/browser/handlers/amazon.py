from .base import Handler


class AmazonHandler(Handler):

    IS_NOISY = True

    @classmethod
    def can_handle(cls, payload: str) -> bool:
        return payload.startswith("https://www.amazon.")

    def get_prepared_url(self) -> str:
        """
        Strip superfluous values from Amazon URLs
        """
        return self.payload[: self.payload.index("?")]

    def post_fetch(self):
        self._click(
            "#dv-action-box > "
            "div > "
            "div > "
            "div > "
            "div.abwJ5F.tFxybk._2LF_6p > "
            "span > "
            "div > "
            "a"
        )
