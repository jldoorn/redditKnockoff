function getAllFeed(user_hash, callback) {
    let posts = [];
    $.getJSON("/api/"+user_hash+"/feed", function(json) {
        $.each(json, function(key, val) {
            posts.push(val);
        })
    }).done(function(){
        callback(posts);
    });
}

Vue.component('post-item',
    {
        props:['post'],
        template:`
        <div class="container pb-3">
        <div class="card shadow">
            <div class="card-body">
                <a :href="'#'">Upvote</a>
                <a :href="'#'">Downvote</a>
                <div class="row align-items-start">
                    <div class="col">{{ post.handle }}</div>
                    <div class="col"><a :href="postLink">{{ post.post_title }}</a></div>
                    <div class="col">Votes:{{ post.post_votes }}</div>
                </div>
                <div class="row align-items-start">
                    <div class="col">{{ post.post_content }}</div>
                </div>
            </div>
            <div class="card-footer text-muted">
                <div class="row">
                    <div class="col">{{ post.time_passed }}</div>
                </div>
            </div>
        </div>
    </div>
        `,
        data: function(){
            return {
                postLink: "/posts/" + this.post.post_id
            }
        }
    })

const app = new Vue( {
    el: '#app',
    data: {
        post: [],
    },
    methods: {}
    ,
    created: function () {
        fetch('/api/'+USERHASH+"/feed")
            .then(response => response.json())
            .then(data => (this.post = data));
    }

})