from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbTypeCategory(CmdbDAO):
    """
    Type category
    """
    COLLECTION = "objects.categories"
    REQUIRED_INIT_KEYS = [
        'name',
        'title',
    ]

    def __init__(self, name, title, **kwargs):
        """
        init category
        :param name: name of category
        :param title: displayed title
        :param type_list: list of all types
        :param sub_categories: selected categories
        :param kwargs: additional data
        """
        self.name = name
        self.title = title
        super(CmdbTypeCategory, self).__init__(**kwargs)

    def get_name(self):
        """
        get name of category
        :return: category name
        """
        return self.name

    def get_title(self):
        """
        get title of category
        :return: category title
        """
        return self.title

    def get_sub_categories(self):
        """
        get all sub categories
        :return: list of all sub categories
        """
        return self.sub_categories

    def get_sub_category(self, name):
        """
        get specific sub category
        :param name: name of selected category
        :return: specific sub category
        """
        return self.sub_categories[name]

    def get_types(self):
        """
        get all types which are in this category
        :return: all types
        """
        return self.type_list

    def get_type(self, name):
        """
        get specific type
        :param name: type name
        :return: selected type
        """
        return self.type_list[name]
