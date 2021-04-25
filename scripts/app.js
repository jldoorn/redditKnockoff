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

Vue.component('pagination',
    {
        props: ['pdata'],
        data: function () {
            return {
                pages: Math.ceil(this.pdata.length / 5),
                currentPage: 1,
                currentSlice: this.pdata.slice(0, 5)
            }
        },
        methods: {
            goToPage: function (pnum) {
                let idx = pnum - 1;
                this.currentPage = pnum;
                this.currentSlice = this.pdata.slice(idx*5, idx*5 + 5);
            },
            nextpage:function(){
                if (this.currentPage < this.pages) {
                    this.currentPage += 1;
                    this.goToPage(this.currentPage);
                }
            },
            prevpage: function (){
                if (this.currentPage > 1) {
                    this.currentPage -=1;
                    this.goToPage(this.currentPage);
                }
            }
        },
        template: `
          <div class="pagination">
            <div class="container">
              <post-item v-for="p in currentSlice"
                         v-bind:key="p.id"
                         v-bind:post="p"></post-item>
            <button v-on:click="prevpage">Prev page</button>
            <button v-on:click="nextpage">Next page</button>
            </div>
            
          </div>
        `
    }
    );

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
        // fetch('/api/'+USERHASH+"/feed")
        //     .then(response => response.json())
        //     .then(data => (this.post = data));
        this.post = [{
            handle: "technojd",
            post_content: "Hurray this is my first post",
            post_creator: "technojd",
            post_id: 1,
            post_timestamp: "2021-04-25 00:06:11",
            post_title: "My first post",
            post_votes: 2,
            time_passed: "Approximately 930 Minutes Ago"
        },{
            handle: "technojd",
            post_content: "Hurray this is my first post",
            post_creator: "technojd",
            post_id: 1,
            post_timestamp: "2021-04-25 00:06:11",
            post_title: "My first post",
            post_votes: 2,
            time_passed: "Approximately 930 Minutes Ago"
        },{
            handle: "technojd",
            post_content: "Hurray this is my first post",
            post_creator: "technojd",
            post_id: 1,
            post_timestamp: "2021-04-25 00:06:11",
            post_title: "My first post",
            post_votes: 2,
            time_passed: "Approximately 930 Minutes Ago"
        },{
            handle: "technojd",
            post_content: "Hurray this is my first post",
            post_creator: "technojd",
            post_id: 1,
            post_timestamp: "2021-04-25 00:06:11",
            post_title: "My first post",
            post_votes: 2,
            time_passed: "Approximately 930 Minutes Ago"
        },{
            handle: "technojd",
            post_content: "Hurray this is my first post",
            post_creator: "technojd",
            post_id: 1,
            post_timestamp: "2021-04-25 00:06:11",
            post_title: "My first post",
            post_votes: 2,
            time_passed: "Approximately 930 Minutes Ago"
        },{
            handle: "technojd",
            post_content: "Hurray this is my first post",
            post_creator: "technojd",
            post_id: 1,
            post_timestamp: "2021-04-25 00:06:11",
            post_title: "My first post",
            post_votes: 2,
            time_passed: "Approximately 930 Minutes Ago"
        },{
            handle: "technojd",
            post_content: "Hurray this is my first post",
            post_creator: "technojd",
            post_id: 1,
            post_timestamp: "2021-04-25 00:06:11",
            post_title: "My first post",
            post_votes: 2,
            time_passed: "Approximately 930 Minutes Ago"
        },{
            handle: "technojd",
            post_content: "Hurray this is my first post",
            post_creator: "technojd",
            post_id: 1,
            post_timestamp: "2021-04-25 00:06:11",
            post_title: "My first post",
            post_votes: 2,
            time_passed: "Approximately 930 Minutes Ago"
        },]
    }

})