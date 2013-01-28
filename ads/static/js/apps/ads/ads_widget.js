define(
    [
        'jquery',
        'underscore',
        'backbone',
        'common',
        './ad_widget'
    ],
    function( $, _, Backbone, Common, AdWidget ) {

        var AdsWidget = Backbone.View.extend({

            tagName: 'section',

            className: 'ads section',

            id: 'ads-section',

            dateFormatFromNow: true,

            initialize: function(options) {
                this.collection.on('reset', this.render, this);
                this.collection.on('add', this.addOne, this);
                _.bindAll(this);
                $(window).on("scroll", this.checkScroll);
                $(window).on("touchmove", this.checkScroll);
                setInterval(this.reRenderTime, 10000);
            },

            checkScroll: function () {
                var triggerPoint = 300;
                if (($(window).scrollTop() + $(window).height() >= $(document).height() - triggerPoint) && !this.collection.ended) {
                    this.loadMore();
                }
            },

            loadMore: function() {
                if (!this.isLoading) {
                    this.isLoading = true;
                    var $loading = this.renderLoading();
                    var that = this;
                    this.collection.fetch({
                        update: true,
                        data: { from: that.collection.last().get("added") },
                        remove: false,
                        success: function(ads, response) {
                            $loading.remove();
                            that.isLoading = false;
                        }
                    });
                }
            },

            render: function() {
                $(this.el).empty();
                if ( this.collection.isEmpty() ) {
                    this.renderEmpty();
                }
                else {
                    this.collection.forEach(this.addOne, this);
                }
                return this;
            },

            addOne: function(model) {
                var adWidget = new AdWidget({ model: model, parentView: this });
                this.$el.append(adWidget.render().el);
            },

            renderEmpty: function() {
                $('<div class="ad">').addClass("nothingfound").text("К сожалению, ничего не найдено").appendTo($(this.el));
            },

            renderLoading: function() {
                var $loading = $('<div class="ad">').addClass("loading").appendTo($(this.el));
                return $loading;
            },

            reRenderTime: function() {
                this.trigger("render:time");
            }

        });

        return AdsWidget;
});
