<template>
    <div>
        <div class="d-flex  justify-content-center" id ="heading">
        <span>
            <h2>
                New Tracker
            </h2>
        </span>
    </div>
    <div class="d-flex  justify-content-center">
<div id="form" class="d-flex flex-column" >
    <div class="card bgforrow">
        <div class="card-body">
<div class="form-group">
        <label class="label" id ="label1">name:</label>
        <input type="text" v-model="name">
    </div>
    <div class="form-group">
        <label class="label" id="label2">description:</label>
            <textarea name="" id="" cols="30" rows="8" v-model="description"></textarea>
    </div>
        <div class="form-group d-flex  justify-content-center">
        <label class="label" id="label2">tracker_type:</label>
           <div>
            <select v-model="tracker_type">
            <option value="numerical">numerical</option>
            <option value="boolean">boolean</option>
            <option value="multichoice">multi-choice</option>
            <option value="timeduration">time-duration</option>
            </select>
            <!-- <input type="text" v-model="tracker_type"> -->
        </div>
    </div>
    <div class="form-group">
        <div v-if="show">
        <label class="label" id="label2">value:</label>
            <input placeholder="eg:one;two;three" type="text" v-model="settings">
        </div>
    </div>
    <div class="form-group">
        <label class="label" id="label2">subs:</label>
            <input type="radio" v-model="subs"  value="1"><span class="forlabel">yes</span>
        <input type="radio" v-model="subs"  value="0"><span class="forlabel">no</span>
    </div>
    <div class="d-flex  justify-content-center">
        <div class="form-group sbbt">
        <button class="btn btn-success btn-md" @click="dosomething">create</button>
      </div>

    </div>
        </div>
    </div>
<div>
</div>
</div>
</div>
    </div>

</template>

<script>
import dateFormat from "dateformat"
export default {
    name:"two",
    data:function(){
    return{
        name:"",
        description:"",
        tracker_type:"numerical",
        settings:"",
        subs:1,
    }
},
methods:{
    dosomething:async function(){
        try {
            console.log("i am called")
            var ts= sessionStorage.getItem("token")
            console.log(ts);
            if((this.settings.match(/^[a-zA-z]+;[a-zA-Z]+;[a-zA-Z]+$/))==null && this.show ){
                alert("Please fill the form correctly.")
                return   
            }
            // alert(dateFormat(new Date(),"dS mmmm yyyy, h:MM:ss TT"));
            var t= await fetch(this.$hostname+"tracker",{
                method:"POST",
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + ts
                  },
                body:JSON.stringify({"uid":1,"name":this.name,"description":this.description,"types":this.tracker_type,"settings":this.settings,"subs":this.subs,"timestamp":""})
            });
            console.log(t)
            var ans= await t.json()
            console.log(ans)
            window.alert("New tracker created")
            this.$router.go(-1)
        } catch (error) {
            console.log(error)
            console.log("oops");
            window.alert(error)  
        }
    }
}
,
mounted:function(){
    var ts= sessionStorage.getItem("token")
    if (ts==null){
        window.alert("no hacking")
        this.$router.push("/one")
    }
},
computed:{
    show:function(){
        if (this.tracker_type=="multichoice"){
            return true
        }
        else{
            return false
        }
    }
}
}
</script>


<style scoped >
#heading{
    margin-top: 15px;
}
select{
    background-color: transparent;
    padding:9px;
    margin: 17px;
    size: 40px;
    font-size: 1.4em;
    border-radius: 20px;
}
.form-group{
    margin: 5%;
}
h1{
    padding-left: 53px;
}

a{
    margin-left: 25%;
}
  .bgforrow{
    box-shadow: 2px 2px 4px 2px rgba(0,0,0,0.2);
    border-radius: 15px;

     color: #1d0244;
    
      padding: 5px;margin: 20px;
  }
  .bgforrow:hover {
box-shadow: 4px 8px 12px 4px rgba(0,0,0,0.4);
}
.card{
    background-color: hsl(0deg 0% 100% / 28%);
} 
.forlabel{
    font-size: 1.5em;
}

 #form{margin-top: 4%;width: 530px;height: 300px;}label{font-size: 1.8em;}h1{margin-top: 40px;text-align: center;}input,textarea{margin-left: 5%;padding: 2px;font-size: 1.5em;border-radius: 20px;background-color: rgba(255, 255, 255, 0.055);}button{font-size: 1.7em;}
</style>