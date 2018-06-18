function gen(target, cssClass, params) {
    var obj = $('#templates .upvote').clone();
    obj.addClass(cssClass);
    $(target).append(obj);
    return obj.upvote(params);
}

$(function() {
        function gen_examples(params) {
            gen('#vote1', '', params);
            gen('#vote2', '', params);
            gen('#vote3', '', params);
            gen('#vote4', '', params);
            gen('#vote5', '', params);
        }
        gen_examples();
        /* var functions = [gen_examples, gen_unix, gen_programmers, gen_serverfault];
                for (var i in functions) {
                    var fun = functions[i];
                    fun();
                    fun({count: 5});
                    fun({count: 6, upvoted: 1});
                    fun({count: 4, downvoted: 1});
                    fun({count: 15, starred: 1});
                    fun({count: 16, upvoted: 1, starred: 1});
                    fun({count: 14, downvoted: 1, starred: 1});
                } */
});