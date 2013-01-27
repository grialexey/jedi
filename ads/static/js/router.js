define(
    [
        'jquery',
        'underscore',
        'backbone'
    ],
    function( $, _, Backbone ) {

        var Router = Backbone.Router.extend({

            routes: {
                "": "lazySearch",
                ":query": "lazySearch"
            },

            initialize: function(options) {
                this.collection = options.collection;
                this.search_widget = options.search_widget;
                this.debounced_search = _.debounce(this.search, 750);
            },

            lazySearch: function(query) {
                this.collection.trigger("search");
//                  var query = decodeURIComponent(query_string.replace(/\+/g, "%20"));
                if (query) {
                    query = decodeURIComponent(query);
                }
                this.search_widget.renderQuery(query);
                this.debounced_search(query);
            },

            search: function(query) {
                this.collection.query = query;
                this.collection.fetch();
            }

        });

        return Router

});