define(
    [
        'jquery',
        'underscore',
        'backbone',
        'text!./templates/search.html',
    ],
    function( $, _, Backbone, searchWidgetTemplate ) {

        var SearchWidget = Backbone.View.extend({

            id: "search-block",

            template: _.template(searchWidgetTemplate),

            events: {
                "keyup #search-input": "searchEventHandler",
                "submit #search-form": "searchEventHandler"
            },

            initialize: function() {
                this.debounced_search = _.debounce(this.search, 750);
                this.collection.on("reset", function() {
                    this.$el.removeClass("loading");
                }, this);
            },

            searchEventHandler: function(event) {
                event.preventDefault();
                var query = this.$el.find(".input").val().trim();
                if (query != this.collection.query) {
                    this.router.navigate(query, {trigger: false});
                    this.lazySearch(query);
                }
            },

            lazySearch: function(query) {
                this.$el.addClass("loading");
                this.debounced_search(query);
            },

            render: function(query) {
                this.$el.html( this.template({ query: query }) );
                return this;
            },

            renderQuery: function(query) {
                this.$el.find(".input").val(query);
            },

            search: function(query) {
                this.collection.query = query;
                this.collection.fetch();
            }


        });

        return SearchWidget;
    });

