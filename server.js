'use strict';
let express = require('express');
let app = express();
let request = require("request");
let sentiment = require('sentiment');
let async = require('async');
let moment = require('moment');
let topGainers = ['Bank Nifty'];
let allData = [],
    totalLength = null,
    lastDate;

app.get('/', function (req, res) {
    function nodeSentiment(page, cb) {
        async.map(topGainers, function (query, callback) {
            var options = {
                method: 'GET',
                url: 'https://newsapi.org/v2/everything',
                qs:
                    {
                        domains: "moneycontrol.com",
                        sources: "google-news-in",
                        sortBy: "publishedAt",
                        q: query,
                        from: '2017-01-01',
                        to: '2017-12-30',
                        page: page,
                        apiKey: 'a26c63b4775146c28523e8344091e19a'
                    },
                headers:
                    {
                        'postman-token': 'a61ed6b0-0b9e-ef48-511d-7830e0bbc3c5',
                        'cache-control': 'no-cache',
                        'content-type': 'application/x-www-form-urlencoded'
                    }
            };
            request(options, function (error, response, body) {
                if (error) throw new Error(error);
                var res = JSON.parse(body);
                // console.log(res);
                if(totalLength === null) {
                    totalLength = res.totalResults;
                }
                if(!!res.articles){
                    callback(null, res.articles);
                }else {
                    callback(error,null);
                }
            });
        }, function (err, result) {
            if (err) {
                console.log(err);
            } else {
                console.log("re" , result[0].length + "---" + totalLength + "---" + allData.length);
                allData.push.apply(allData, result[0]);
                if (totalLength > allData.length) {
                    nodeSentiment(lastDate, cb);
                } else {
                    // console.log('----',allData);
                    // var dateArray = [];
                    var obj={};
                    // allData=allData.filter(function (item) {
                    //     var regex= new RegExp(topGainers[0], 'gi');
                    //     return item && item.title && item.description && (regex.test(item.title) || regex.test(item.description));
                    // });
                    allData.forEach(item => {
                        if(!obj[moment(item.publishedAt).format('DD-MM-YYYY')]){
                            obj[moment(item.publishedAt).format('DD-MM-YYYY')]=[];
                        }
                        var newsType;
                        var titleSentiment = sentiment(item.title).score;
                        var descSentiment = sentiment(item.description).score;
                        // console.log(moment(item.publishedAt).format('DD-MM-YYYY'));
                        if(descSentiment ==0){
                            newsType='Neutral'
                        }else if(descSentiment>0 &&descSentiment<=5){
                            newsType='Buy'
                        }else if(descSentiment>5 &&descSentiment<=10){
                            newsType='Strong Buy'
                        }else if(descSentiment>=-5 &&descSentiment<0){
                            newsType='Sell'
                        }else if(descSentiment>-5 &&descSentiment<=-10){
                            newsType='Strong Sell'
                        }
                        obj[moment(item.publishedAt).format('DD-MM-YYYY')].push({
                            date : item.publishedAt,
                            title : item.title,
                            desc : item.description,
                            link : item.link,
                            descSentiment2 : descSentiment,
                            newsType: newsType
                        });
                    });
                    // console.log('obj----->>',obj);

                    cb(obj);
                }

            }
        });
    }
    nodeSentiment(1, (data) => {
        console.log(JSON.stringify(data));
        console.log('Done');
        res.send(data);
    });
});
app.listen(3000);