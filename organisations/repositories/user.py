from organisations.models import User,Organisations


class UserRepository:

    @classmethod
    def create(cls, user):
        created_user = User(
            username=user.get("username"),
            email=user.get("email"),
            organisation=Organisations.objects.get(id=user.get("organisation")),
            account_type= user.get("account_type"),
            avatar= user.get("avatar"),
            is_active= user.get("is_active"),
        )
        created_user.set_password(user.get("password"))
        created_user.save()
        return created_user

    @classmethod
    def find_one(cls, user_id):
        return User.objects.get(id=user_id)

    @classmethod
    def find_by_username(cls, username):
        return User.objects.get(username=username)

    @classmethod
    def find_all(cls):
        return User.objects.all()

    # @classmethod
    # def update(cls, user_id, user_data):
    #     user = cls.find_one(user_id)
    #     user.email = user_data.get("email")
    #     user.password = user_data.get("password")
    #     user.username = user_data.get("username")
    #     user.account_type = user.get("account_type")
    #     user.avatar = user.get("avatar"),
    #     user.is_active = user.get("is_active")
    #
    #     return user.save()

    @classmethod
    def delete(cls, user_id):
        user = cls.find_one(user_id)
        user.delete()

    @classmethod
    def update_as_admin(cls, user_id, user_data):
        user = cls.find_one(user_id)
        user.email = user_data.get("email")
        user.username = user_data.get("username")
        user.account_type = user_data.get("account_type")

        if user_data.get("password") is not None and len(user_data.get("password")) > 0:
            user.set_password(user_data.get("password"))

        if user_data.get("avatar") is not None :
            user.avatar = user_data.get("avatar")

        user.is_active = user_data.get("is_active")

        return user.save()

    @classmethod
    def update_as_manager(cls, user_id, user_data):
        user = cls.find_one(user_id)
        user.password = user_data.get("password")
        user.avatar = user.get("avatar")
        return user.save()
