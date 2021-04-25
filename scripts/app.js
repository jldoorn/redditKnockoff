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
        data: function () {
            return {
                pdata: [],
                pages: 0,
                currentPage: 1,
                currentSlice: [],
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
            },
            upvote: function (postid) {
                fetch('/'+USERHASH+"/vote/"+postid+"/up")
                    .then(response => response.json())
                    .then(data => (this.updatevote(postid, data.tally)));
            },
            downvote: function (postid) {
                fetch('/'+USERHASH+"/vote/"+postid+"/down")
                    .then(response => response.json())
                    .then(data => (this.updatevote(postid, data.tally)));
            },
            updatevote: function(postid, votes) {
                let found = this.pdata.findIndex(element => element.post_id === postid);
                this.pdata[found].post_votes = votes;
                this.initData(this.pdata);
            },
            initData: function (data) {
                let idx = this.currentPage -1;
                this.pdata = data;
                this.pages = Math.ceil(this.pdata.length / 5);
                this.currentSlice =  this.pdata.slice(idx*5, idx*5 + 5);
            }
        },
        template: `
          <div class="pagination">
            <div class="container">
              <post-item v-for="p in currentSlice"
                         v-bind:key="p.id"
                         v-bind:post="p"
                          v-on:upvote="upvote"
                          v-on:downvote="downvote"></post-item>
            <button v-on:click="prevpage">Prev page</button>
            <button v-on:click="nextpage">Next page</button>
            </div>
            
          </div>
        `,
        created: function () {
            fetch('/api/'+USERHASH+"/feed")
                .then(response => response.json())
                .then(data => (this.initData(data)));
            // this.pdata = [{
            //     handle: "technojd",
            //     post_content: "Hurray this is my first post",
            //     post_creator: "technojd",
            //     post_id: 1,
            //     post_timestamp: "2021-04-25 00:06:11",
            //     post_title: "My first post",
            //     post_votes: 2,
            //     time_passed: "Approximately 930 Minutes Ago"
            // },{
            //     handle: "technojd",
            //     post_content: "Hurray this is my first post",
            //     post_creator: "technojd",
            //     post_id: 2,
            //     post_timestamp: "2021-04-25 00:06:11",
            //     post_title: "My first post",
            //     post_votes: 2,
            //     time_passed: "Approximately 930 Minutes Ago"
            // },{
            //     handle: "technojd",
            //     post_content: "Hurray this is my first post",
            //     post_creator: "technojd",
            //     post_id: 3,
            //     post_timestamp: "2021-04-25 00:06:11",
            //     post_title: "My first post",
            //     post_votes: 2,
            //     time_passed: "Approximately 930 Minutes Ago"
            // },{
            //     handle: "technojd",
            //     post_content: "Hurray this is my first post",
            //     post_creator: "technojd",
            //     post_id: 4,
            //     post_timestamp: "2021-04-25 00:06:11",
            //     post_title: "My first post",
            //     post_votes: 2,
            //     time_passed: "Approximately 930 Minutes Ago"
            // },{
            //     handle: "technojd",
            //     post_content: "Hurray this is my first post",
            //     post_creator: "technojd",
            //     post_id: 5,
            //     post_timestamp: "2021-04-25 00:06:11",
            //     post_title: "My first post",
            //     post_votes: 2,
            //     time_passed: "Approximately 930 Minutes Ago"
            // },{
            //     handle: "technojd",
            //     post_content: "Hurray this is my first post",
            //     post_creator: "technojd",
            //     post_id: 6,
            //     post_timestamp: "2021-04-25 00:06:11",
            //     post_title: "My first post",
            //     post_votes: 2,
            //     time_passed: "Approximately 930 Minutes Ago"
            // },{
            //     handle: "technojd",
            //     post_content: "Hurray this is my first post",
            //     post_creator: "technojd",
            //     post_id: 7,
            //     post_timestamp: "2021-04-25 00:06:11",
            //     post_title: "My first post",
            //     post_votes: 2,
            //     time_passed: "Approximately 930 Minutes Ago"
            // },{
            //     handle: "technojd",
            //     post_content: "Hurray this is my first post",
            //     post_creator: "technojd",
            //     post_id: 8,
            //     post_timestamp: "2021-04-25 00:06:11",
            //     post_title: "My first post",
            //     post_votes: 2,
            //     time_passed: "Approximately 930 Minutes Ago"
            // },];

        }
    }
    );

Vue.component('post-item',
    {
        props:['post'],
        template:`
        <div class="container pb-3">
        <div class="card shadow">
            <div class="card-body">
                <a :href="'#'" v-on:click="$emit('upvote', post.post_id)">Upvote</a>
                <a :href="'#'" v-on:click="$emit('downvote', post.post_id)">Downvote</a>
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
    data: {},
    methods: {},
})