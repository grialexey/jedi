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
                "keyup #search-input": "search",
                "submit #search-form": "search"
            },

            initialize: function() {
                this.collection.on("reset", function() {
                    this.$el.removeClass("loading");
                }, this);
                this.collection.on("search", function() {
                    this.$el.addClass("loading");
                }, this);
            },

            search: function(event) {
                event.preventDefault();
                this.router.navigate(this.getQuery(), {trigger: true});
            },

            render: function(query) {
                this.$el.html( this.template({ query: query }) );
                return this;
            },

            renderQuery: function(query) {
                this.$el.find(".input").val(query);
            },

            getQuery: function() {
                var query = this.$el.find(".input").val().trim();
//                var encoded_query = encodeURIComponent(query).replace(/%20/g, "+");
                return query
            }

        });

        return SearchWidget;
    });

