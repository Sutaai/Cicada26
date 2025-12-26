class Headers:
    @staticmethod
    def location(description: str):
        return {
            "Location": {
                "description": description,
                "schema": {"type": "string"},
            }
        }
