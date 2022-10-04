

<template>

<div v-if="loaded">
        <div>
          <div class="row firstrow">
    <div class="col-7">
    <h1>
            Hello,{{name}}
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
        
<div class="d-flex  justify-content-center" id="content">
    <div class="card bgforrow">
        <div class="card-body">
            <div class="pseudo">
<div  class="container">
<div class="row">
                <div class="col-3">
                        Tracker
                </div>
                <div class="col-3">
                       LastTracked
                </div>
</div>
<hr>
<div>
    <div v-if="list.length!=0" >
        <div v-for="each in list">
<trackerdisplay v-bind:summa="each" v-bind:style="style" @refresh="refresh"  ></trackerdisplay>
    </div>
    </div>
    <div v-else class="d-flex  justify-content-center" id="texting">
                <h2>
                    No logs available. 
        Create a new tracker to get started
                </h2>
            </div>
</div>
</div>
</div>
            </div>
        </div>
    </div>
</div>
<div class="d-flex  justify-content-center" >

<div>
    <a href="#/two" class="btn btn-primary btn-md" role="button">Add a new tracker</a>
</div>


</div>

</div>

    
</template>

<script>

import trackerdisplay from '../components/trackerdisplay.vue' 
var ts= sessionStorage.getItem("token")
export default {
    components:{
        trackerdisplay,
    },
    computed:{
link:function(){
    return this.$hostname+"exporttracker/"+sessionStorage.getItem("token")
}
},
    name:"three",
    data:function(){
        return {
            list:[],
            loaded:false,
            style:{
                "padding": "1%",

            },
            name:sessionStorage.getItem("name")
        }
    },
    mounted:async function(){
    var ts= sessionStorage.getItem("token")
    if (ts==null){
        window.alert("no hacking")
        this.$router.push("/one")
    }
    var t= await fetch(this.$hostname+"tracker",{
                    method:"GET",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                      },    
                });
    this.list=await t.json();
    this.loaded=true;
},
methods:{
    upload: async function(event){
        var ts= sessionStorage.getItem("token")
        try {
            console.log(event)
            var input=event.target.files;
            const form= new FormData()
            form.append("tracker",input[0])
                var t= await fetch(this.$hostname+"importtracker",{
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
dosomething:async function(t_id){
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
    var ts= sessionStorage.getItem("token")
    var t= await fetch(this.$hostname+"tracker",{
                    method:"GET",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                      },    
                });
    this.list=await t.json();
    
},
refresh:async function()
{
     var ts= sessionStorage.getItem("token")
    console.log("i am called from sub componenet")
    var t= await fetch(this.$hostname+"tracker",{
                    method:"GET",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                      },    
                });
    this.list=await t.json();

},
logoff:function(){
    sessionStorage.removeItem("token")
},
down:async function(){
    var ts= sessionStorage.getItem("token")
    var t= await fetch(this.$hostname+"exporttracker/"+ts,{
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
}
},

}
</script>
<style scoped>
h1{
    padding-left: 53px;
}
.row{
    margin-bottom: 3%;
    
}
.space{
    padding-left: 74px;
}
#texting{
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
.card{
    background-color: hsl(0deg 0% 100% / 28%);
}
.firstrow{
    margin-top: 30px;
}
/* .pseudo{
    overflow-y: scroll;
} */
#content{
    height: 500px;
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
#upward{
    color:white
}
</style>