<template>
    <div>
        <div class="d-flex  justify-content-center firstrow">
        <div>
            <h2>
                New Log
            </h2>
        </div>
    </div>
    <div class="d-flex  justify-content-center">
<div id="form" class="d-flex flex-column" >
    <div class="card bgforrow">
        <div class="card-body">
<div class="form-group">
        <label class="label" id ="label1">Value:</label>
        <div v-if="trackerdetails.types=='numerical'">
            <input type="number" v-model="value">
        </div>
        <div v-if="trackerdetails.types=='boolean'">
            <input type="radio" v-model="value" value="true"><span>true</span>
            <input type="radio" v-model="value" value="false"><span>false</span>
        </div>
        <div v-if="trackerdetails.types=='multichoice'">
            <select v-model="value"  >
            <option :value="i" v-for="i in trackerdetails.settings.split(';')" >{{i}}</option>
            </select>
            <!-- <input type="text" v-model="tracker_type"> -->
        </div>
        <div v-if="trackerdetails.types=='timeduration'">
            <input type="time" v-model="value">
        </div>
    </div>
    <div class="form-group">
        <label class="label" id="label2">note:</label>
            <input type="text" v-model="note">
    </div>
        <div class="form-group">
        <label class="label" id="label2">Timestamp</label>
           <input type="datetime-local"  v-model="timestamp">
    </div>
    <div class="d-flex  justify-content-center">
<div class="form-group sbbt">
        <button class="btn btn-success" @click="dosomething">log</button>
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
import store from "@/store"
export default {
    name:"newlog",
    data:function(){
    return{
        value:"",
        note:"",
        trackerdetails:{},
        // s:store.state.currenttracker,
        // op:store.state.currenttracker.settings.split(";"),
        timestamp:new Date()
        // tracker_type:"",
        // tracker_value:""
    }
},
methods:{
    dosomething:async function(){
        try {
            var ts= sessionStorage.getItem("token")
            console.log(ts);
            if (this.trackerdetails.types=="timeduration"){
                this.value=this.minval
            }
            if(this.value=="" || this.note==""){
                alert("please enter the details")
                return
            }
            // alert(dateFormat(new Date(),"dS mmmm yyyy, h:MM:ss TT"));
            var t= await fetch(this.$hostname+"log",{
                method:"POST",
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + ts
                  },
                body:JSON.stringify({"value":this.value,"note":this.note,"tracker":this.$route.params.tid,"timestamp":this.finaltime})
            });
            console.log(t)
            var ans= await t.json()
            console.log(ans)
            window.alert("the entry has been logged successfully")
            this.$router.go(-1)
        } catch (error) {
            console.log(error)
            console.log("oops");
            window.alert(error)  
        }
    }
}
,
mounted:async function(){
    var ts= sessionStorage.getItem("token")
    if (ts==null){
        window.alert("no hacking")
        this.$router.push("/one")
    }
    var t= await fetch(this.$hostname+`logview/${this.$route.params.tid}`,{
                    method:"GET",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                        },    
                });
    this.trackerdetails=await t.json();
},
computed:{
    limit:function(){
        return new Date().toISOString()
    },
    minval:function(){
        let s= this.value.split(":")
        return (Number.parseInt(s[0])*60)+Number.parseInt(s[1])
    },
        finaltime:function(){
            let midddate= new Date(this.timestamp)
            console.log(midddate.getTime())
            return (midddate.getTime()/1000)
        },
}
}
</script>


<style scoped >
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
.firstrow{
    margin-top: 15px;
}
span{
    font-size: 1.5em;
}
/* .sbbt{
    padding-left: 20%;
} */
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

 #form{margin-top: 3%;width: 436px;height: 300px;}label{font-size: 1.8em;}h1{margin-top: 40px;text-align: center;}input{margin-left: 5%;padding: 2px;font-size: 1.5em;border-radius: 20px;background-color: rgba(255, 255, 255, 0.055);}button{font-size: 1.6em;}
</style>


















