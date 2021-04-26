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
        props: ['feed'],
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
            },
            handleDelete: function(postid){
                let found = this.pdata.findIndex(element => element.post_id === postid);
                this.pdata.splice(found,1);
                this.initData(this.pdata);
            },
            deletepost: function (postid) {
                fetch("/api/"+USERHASH+"/delete/"+postid).then(response => this.handleDelete(postid));
            }
        },
        template: `
          <div class="pagination">
            <div class="container">
              <post-item v-for="p in currentSlice"
                         v-bind:key="p.id"
                         v-bind:post="p"
                         v-bind:feed="feed"
                          v-on:upvote="upvote"
                          v-on:downvote="downvote"
                          v-on:deletepost="deletepost"></post-item>
            <nav aria-label="...">
            <ul class="pagination">
            <li class="page-item">
            <a href="#" v-on:click="prevpage" class="page-link">Previous</a>
</li>
<li class="page-item">
<a href="#" v-on:click="nextpage" class="page-link">Next</a>
</li>
</ul>
</nav>
           
            </div>
            
          </div>
        `,
        created: function () {
            let handle = "";
            if (this.feed) {
                handle = "feed";
            } else {
                handle = "profile";
            }
            fetch('/api/'+USERHASH+"/"+handle)
                .then(response => response.json())
                .then(data => (this.initData(data)));

        }
    }
    );

Vue.component('post-item',
    {
        props:['post', 'feed'],
        template:`
        <div class="container pb-3">
        <div class="card shadow">

            <div class="card-body">
                <a class="card-title h4" :href="postLink">{{ post.post_title }}</a>
                <h6 class="card-subtitle mb-2 text-muted">{{ post.handle }}</h6>

                <div class="card-text">
                    <div class="row">
                        <div class="col-md-auto">
                        <a href="#" class="bi bi-arrow-bar-up" v-if="feed" v-on:click="$emit('upvote', post.post_id)"></a>
                        <div class="col">Votes: {{ post.post_votes }}</div>
                        <a href="#" class="bi bi-arrow-bar-down" v-if="feed" v-on:click="$emit('downvote', post.post_id)"></a>
                    </div>
                        <div class="col">
                    {{ post.post_content }}</div>
                    </div>
                </div>
            </div>
            <div class="card-footer">
                <div class="row">
                    <div class="col">
                        {{ post.time_passed }}
                    </div>
                    <div class="col">
                        <button class="btn btn-primary float-end" v-on:click="$emit('deletepost', post.post_id)" v-if="!feed">Delete Post</button>
                    </div>
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