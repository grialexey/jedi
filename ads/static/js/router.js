define(
    [
        'jquery',
        'underscore',
        'backbone'
    ],
    function( $, _, Backbone ) {

        var Router = Backbone.Router.extend({

            routes: {
                "": "search",
                ":query": "search"
            },

            initialize: function(options) {
                this.search_widget = options.search_widget;
            },

            search: function(query) {
                if (query) {
                    query = decodeURIComponent(query);
                }
                this.search_widget.renderQuery(query);
                this.search_widget.search(query);
            }

        });

        return Router

});