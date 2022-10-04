<template>
<div>
    <div class="container">
        <div class="row">
            <div class="col text-wrap">
                <a id="specificlink" @click="pushdata(summa)">{{summa.name}}</a>
            </div>
            <div v-if="summa.timestamp!=''" class="col">
                {{summa.timestamp}}
            </div>
            <div v-else class="col">
                Yet to log
            </div>
            <div class="col">
                      <span><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-plus-fill" viewBox="0 0 16 16">
  <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0zM9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1zM8.5 7v1.5H10a.5.5 0 0 1 0 1H8.5V11a.5.5 0 0 1-1 0V9.5H6a.5.5 0 0 1 0-1h1.5V7a.5.5 0 0 1 1 0z"/>
</svg> <router-link    :to="{name:'addlog',params:{tid:summa.tid}}">New log</router-link></span>
            </div>
            <div class="col">
                <div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton2" data-bs-toggle="dropdown" aria-expanded="false">
    Actions
  </button>
  <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton2">
    <li><a class="dropdown-item " role="button" @click="dosomething">Edit</a></li>
    <li><a class="dropdown-item" role="button" @click="doesomething(summa.tid)" >Delete</a></li>
  </ul>
</div>
            </div>
        </div>
        
    <div v-show="visible" class="row" id="edit">
    <div class="col">
    name: <input type="text" :placeholder=summa.name v-model="name">
    </div>
 <div class="col">
    description: <input type="text" :placeholder=summa.description v-model="description">
                </div>
 <div class="col">
    Notification:
<div>
    <input type="radio" v-model="modelforsubs" value="1">yes
<input type="radio" v-model="modelforsubs" value="0">no
</div>
                </div>
                 <div class="col">
            <button class="btn btn-success btn-md" @click="backcall(summa.tid,event)">submit</button>
                </div>
    </div>
    </div>
    </div>
</template>

<script>
import store from '@/store';
export default {
    name:"trackerdisplay",
    data() {
        return {
            name:"",
            description:"",
            modelforsubs:"",
            visible:false,
        }
    },
    props:["summa"],
    methods: {
        pushdata:function(summa){
            store.commit("settracker",summa)
            this.$router.push({name:'logview',params:{tid:summa.tid}})
        },
        dosomething:function(){
            if (this.visible===true){
                this.visible=false;
            }
            else{
                this.visible=true;
                this.name=this.summa.name
                this.description=this.summa.description
                this.modelforsubs=this.summa.subs
            }
           
        },
        backcall: async function(id,event){
console.log("i am called");
    var ts= sessionStorage.getItem("token")
    if (ts==null){
        window.alert("no hacking")
        this.$router.push("/one")
    }
    console.log(EventSource.bind)
    console.log(this.name)
    var t= await fetch(this.$hostname+"trackercrud/"+id,{
                    method:"PUT",
                    
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                      },
                    body:JSON.stringify({"name":this.name,"description":this.description,"subs":this.modelforsubs})
                });
                console.log(t)
                var ans= await t.json()
                this.summa.name=this.name
                this.summa.description=this.description
                this.visible=false
                this.summa.subs=this.modelforsubs

                // this.$emit("refresh")
                // window.alert(ans.token) 
                // sessionStorage.setItem("token",ans.token);
                // this.$router.push("/three")
            } ,
            doesomething:async function(t_id){
    console.log("i am called")
    var ts= sessionStorage.getItem("token")
            console.log(ts);
            var t= await fetch(this.$hostname+"trackercrud/"+t_id,{
                    method:"DELETE",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                        },    
                });
                var ans=await t.json();
                this.$emit("refresh")
},

    },
}
</script>
<style scoped>
li:hover{
    background-color: rgba(49, 49, 148, 0.822);
}
#edit{
    margin-top: 20px;
}
.over{
    margin-left: 10px;
    padding-left: 15px;
    margin-bottom: 15px;
}
#specificlink{
    color: blue;
    text-decoration: none;
}
a{
    color: blue;
    text-decoration: none;
}
a:hover{
    text-decoration: underline;
}
#specificlink:hover{
    cursor: pointer;
    text-decoration: underline;

}
</style>