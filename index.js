'use strict';

let Parser = require('rss-parser');
let path= require('path');
let parser = new Parser();
let PythonShell = require('python-shell');
let pythonScriptPath=path.join(__dirname, './script');
(async () => {
    // let feed = await parser.parseURL('http://www.moneycontrol.com/rss/buzzingstocks.xml');
    // console.log(feed.title);
    // console.log('Total news:--->>>',feed.items.length);
    // var array=[];
    // feed.items.forEach(item => {
    //     var obj={};
    //     // console.log('------>>Date::',item.pubDate);
    //     // console.log('------>>Title::',item.title);
    //     // console.log('------>>Content::',item.content);
    //     obj.date=item.pubDate;
    //     obj.titel= item.title;
        var options = {
            mode: 'text',
            pythonOptions: ['-u'],
            scriptPath: pythonScriptPath,
            args: [text]
        };
        PythonShell.run("sentiment.py", options, function (err, results) {
            if (err) {
            } else {
                console.log(results[0]);
                obj.sentiment=results[0];
            }
        });
    //     array.push(obj);
    // });
    // console.log(array);
})();
