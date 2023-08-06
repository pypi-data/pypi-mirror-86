from datasette.app import DatasetteRouter


def patch_datasette():
    """
    Monkey patching for original Datasette
    """

    def router_init(self, datasette, routes):
        routes.append((
            TableView.as_view(self),
            r"/(?P<db_name>[^/]+)/(?P<table_and_format>[^/]+?$)",
        ))
        self.original_router_init(datasette, routes)

    DatasetteRouter.original_router_init = DatasetteRouter.__init__
    DatasetteRouter.__init__ = router_init
