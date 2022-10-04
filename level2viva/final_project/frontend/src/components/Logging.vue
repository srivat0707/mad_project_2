<template>
   <div v-if="loaded">
    <div class="row firstrow">
    <div class="col-7">
    <h1>
            {{this.trackerdetails.name}}
        </h1>
    </div>
    <div class="col">
        <input id="file" class="inputfile" type="file" name="file" accept=".csv" @change="upload" >
        <label for="file" class="btn  btn-md btn-success"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud-upload" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"/>
  <path fill-rule="evenodd" d="M7.646 4.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707V14.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3z"/>
</svg> upload</label>
    </div>
    <div class="col">
    <button class="btn btn-success btn-md" @click="down">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
  <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
  <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
</svg>  download</button>
    </div>
    <div class="col">
      <router-link to="/logout" class="btn btn-success btn-md" role="button" >logoff</router-link>
    </div>
  </div>
    <!-- <button><a :href=this.link download="">csv download</a></button> -->
         <!-- <div class="d-flex  justify-content-center">
            <h1> {{this.trackerdetails.name}} .......</h1>
         </div> -->
         <div>
            <h4>
                Description:
            </h4>
         </div>
         <div>
            <h5>
                {{this.trackerdetails.description}}
            </h5>
         </div>
        <div id="chart" v-if="list.length!=0">
            <customchart v-bind:data="this.list" v-bind:type="this.trackerdetails.types" v-if="list" class="special"></customchart>
        </div>
        <div v-else class="d-flex  justify-content-center spaces">
            <h2>
                No data to available to plot a graph.😒
            </h2>
        </div>
        <div class="d-flex  justify-content-center space spaces" >
            <h2>Logs</h2>
        </div>


<div class="d-flex  justify-content-center" id="content">
    <div class="card bgforrow">
        <div class="card-body">
            <div class="pseudo" v-if="list.length!=0">
<div  class="container">
<div class="row">
                <div class="col-2">
                           On
                </div>
                <div class="col-2">
                           Value
                </div>
</div>
<hr>
<div >
<div v-for="i in list"  >
    <logdisplay v-bind:summa="i"  v-bind:style="style" @refresh="refresh" ></logdisplay>    
    </div>
    </div>
<!-- <div v-else>
                No logs available. Create a new one
            </div> -->
        </div>
    </div>
    <div v-else id="texting" class="spaces">
        <h2>
            No logs available. Create a new one
        </h2>
    </div>
</div>

</div>
   </div>
   <div class="d-flex  justify-content-center" >

<div>
    <router-link    :to="{name:'addlog',params:{tid:this.trackerdetails.tid}}" role="button" class="btn btn-primary btn-md">New log</router-link>
</div>
</div>
   </div>

















    
<!-- <a href="#/two">add new entry</a> -->
</template>

<script>
import logdisplay from './logdisplay.vue'
import customchart from "./pie.vue"
import store from '@/store';
import { Store } from 'vuex';
export default {
    // props:["tid"],
    name:"logging",
    components:{
    logdisplay,
    customchart
},
data:function(){
    return{
        loaded:false,
        list:[],
        newlist:[],
        val:"numerical",
        options:{
             hAxis: { textPosition: 'none' },
        },
        trackerdetails:{}
    }
},
computed:{
link:function(){
    return this.$hostname+"exportlog/"+this.$route.params.tid+"/"+sessionStorage.getItem("token")
},

},
    async mounted() {
    var ts= sessionStorage.getItem("token")
    if (ts==null){
        window.alert("no hacking")
        this.$router.push("/one")
    }
    // alert(this.$route.params.tid);
    // alert(this.$route.params.type);
    var tsd= await fetch(this.$hostname+`log/${this.$route.params.tid}`,{
                    method:"GET",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                        },    
                });
    this.list=await tsd.json();
    var t= await fetch(this.$hostname+`logview/${this.$route.params.tid}`,{
                    method:"GET",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                        },    
                });
    this.trackerdetails=await t.json();
    this.loaded=true;


},
methods:{
dosomething:async function(t_id){
    console.log("i am called")
    var ts= sessionStorage.getItem("token")
            console.log(ts);
            var t= await fetch(this.$hostname+"logcrud/"+t_id,{
                    method:"DELETE",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                        },    
                });
                var ans=await t.json();
    // window.alert(ans);
    var t= await fetch(this.$hostname+`log/${this.$route.params.tid}`,{
                    method:"GET",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                        },    
                });
    this.list=await t.json();
},
upload: async function(event){
        var ts= sessionStorage.getItem("token")
        try {
            console.log(event)
            var input=event.target.files;
            const form= new FormData()
            form.append("tracker",input[0])
                var t= await fetch(this.$hostname+"importlog",{
                    method:"POST",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                      },
                    body:form
                });
                console.log(t)
                var ans= await t.text()
                alert("the file has been sent")
                if (!t.ok){
                    alert(ans.message)
}        
            } catch (error) {
                console.log(error)
                console.log("oops");
                window.alert(error)  
            }
    },
down:async function(){
    var ts= sessionStorage.getItem("token")
    var t= await fetch(this.link,{
                    method:"GET",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                      },    
                });
    console.log(t)
    if (t.ok){
        alert("the email will be sent out soon. 😊")
    }
},
refresh:async function(){
    
var ts= sessionStorage.getItem("token")
    if (ts==null){
        window.alert("no hacking")
        this.$router.push("/one")
    }
    // alert(ts);
    // alert("sending request")
    var t= await fetch(this.$hostname+`log/${this.$route.params.tid}`,{
                    method:"GET",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                        },    
                });
    this.list=await t.json();
}
}
}
</script>

<style scoped>
h1,h4,h5{
    padding-left: 53px;
}
.special{
    background-color: rgba(253, 250, 250, 0.215);
}
#chart{
    padding: 20px;
    margin: 30px;
}
.row{
    margin-bottom: 3%;
    
}
.space{
    padding-left: 65px;
}
#tetxing{
    margin-top: 25px;
}
.bgforrow{
    box-shadow: 2px 2px 4px 2px rgba(0,0,0,0.2);
    border-radius: 15px;
 overflow-y: auto;
     color: #1d0244;
    
      padding: 5px;margin: 20px;
  }
  .bgforrow:hover {
box-shadow: 4px 8px 12px 4px rgba(0,0,0,0.4);
}
.inputfile{
    opacity:0;
    z-index:-1;
    overflow:hidden;
    position:absolute;
    width:0.1px;
    height: 0.1px;
}
.inputfile + label{
    font-size: 1rem;
    font-weight: 400;
    color: white;
    background-color: #198754;
    display: inline-block;
}
.inputfile:focus + labe,
.inputfile + label:hover{
    cursor: pointer;
}
.firstrow{
    margin-top: 30px;
}
.spaces{
    margin-top: 20px;
}
.card{
    background-color: hsl(0deg 0% 100% / 28%);
}

#content{
    height: 500px;

    
}
</style>