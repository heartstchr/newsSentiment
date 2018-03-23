var google = require('google');

google.resultsPerPage = 25;
var nextCounter = 0;

google('upstox', function (err, res) {
    if (err) console.error(err);
    // console.log('----------');
    // console.log(res.links);
    // console.log('----------');
    for (var i = 0; i < res.links.length; ++i) {
        var link = res.links[i];
        // console.log(link.title + ' - ' + link.href);
        // console.log(link.description + "\n")
    }

    if (nextCounter < 0) {
        nextCounter += 1;
        if (res.next) res.next()
    }
});
