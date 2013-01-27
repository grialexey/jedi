require.config({
    shim: {
        'underscore': {
            exports: '_'
        },
        'backbone': {
            deps: [
                'underscore',
                'jquery'
            ],
            exports: 'Backbone'
        },
        'momentjs': {
            exports: 'moment'
        }
    },
    paths: {
        jquery: 'libs/jquery/jquery.min',
        underscore: 'libs/underscore/lodash.min',
        backbone: 'libs/backbone/backbone-min',
        text: 'libs/require/text',
        momentjs: 'libs/moment/moment.min'
    }
});

require(
	[
		'jquery',
        'backbone',
        'apps/ads/ads_collection',
        'apps/ads/search_widget',
        'apps/ads/ads_widget',
        'router'
	],
	function( $, Backbone, AdsCollection, SearchWidget, AdsWidget, Router ) {
        var sell_ads = new AdsCollection();
        var search_widget = new SearchWidget({ collection: sell_ads });
        search_widget.router = new Router({ collection: sell_ads, search_widget: search_widget });
        var ads_widget = new AdsWidget({ collection: sell_ads });
        Backbone.history.start({ pushState: true, silent: true });

        $(document).ready(function() {
            search_widget.render(bootstrap.query).$el.appendTo('header');
            ads_widget.$el.appendTo("#content");
            sell_ads.query = bootstrap.query;
            sell_ads.ended = bootstrap.ended;
            sell_ads.reset(bootstrap.ads);
        });

});