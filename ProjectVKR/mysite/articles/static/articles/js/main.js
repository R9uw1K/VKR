function exportArticle(article_id, id_) {
            console.log(article_id, id_)
            var articleId = article_id; // Здесь нужно указать идентификатор статьи
            var format = document.querySelectorAll('select')[id_*2-2].value;
            var url = '/export/' + format + '/' + articleId + '/';
            location.href=url;
        }
function normaliseArticle(article_id, id_) {
        console.log(article_id, id_)
        var articleId = article_id; // Здесь нужно указать идентификатор статьи
        console.log(document.querySelectorAll('select'));
        var format = document.querySelectorAll('select')[id_*2-1].value;
        var url = '/normalize/' + format + '/' + articleId + '/';
        location.href=url;
}