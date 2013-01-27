define(
    [
        'underscore',
        'backbone',
        './ad_model'
    ],
    function( _, Backbone, AdModel ) {

        var AdsCollection = Backbone.Collection.extend({

            model: AdModel,

            // Загружено ли последнее объявление
            ended: false,

            // Какому поисковому запросу принадлежать объявления
            query: "",

            url: function() {
                if (this.query) {
                    return "/" + this.query;
                }
                else {
                    return "/"
                }
            },

            parse: function(response) {
                this.ended = response.ended;
                return response.ads;
            },

            comparator: function(ad) {
                var added = new Date(ad.get("added"));
                return -added;
            }

        });

        return AdsCollection;

    });