define(
    [
        'jquery',
        'underscore',
        'backbone',
        'common',
        'text!./templates/ad.html'
    ],
    function( $, _, Backbone, Common, adTemplate ) {

        var AdWidget = Backbone.View.extend({

            tagName:  'article',

            className: 'ad',

            template: _.template( adTemplate ),

            opened: false,

            events: {
                "click .info": "toggleDescription",
                "click .date .time": "toggleDateTimeFormat",
            },

            initialize: function(options) {
                this.parentView = options.parentView;
                this.parentView.on("render:time", this.renderTime, this);
            },

            render: function() {
                this.$el.html( this.template({
                    ad: this.model.toJSON(),
                    opened: this.opened
                }));
                this.renderTime();
                return this;
            },

            renderTime: function() {
                var isFromNow = this.parentView.dateFormatFromNow;
                var dateFormatted = null;
                var added = this.model.get('added');
                if (isFromNow) {
                    dateFormatted = Common.moment(added).from(new Date());
                }
                else {
                    dateFormatted = Common.moment(added).calendar(new Date());
                }
                this.$el.find(".date .time").text(dateFormatted);
            },

            toggleDescription: function(event) {
                event.preventDefault();
                this.opened = !this.opened;
                this.$el.find('.description').slideToggle(200)
            },

            toggleDateTimeFormat: function(event) {
                event.preventDefault();
                event.stopImmediatePropagation();
                this.parentView.dateFormatFromNow = !this.parentView.dateFormatFromNow;
                this.parentView.trigger("render:time");
            }

        });

        return AdWidget;
});