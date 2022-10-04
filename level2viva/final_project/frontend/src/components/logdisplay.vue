<template>
<div>
    <div class="container">
        <div class="row" id="one">
            <div class="col">
                {{summa.timestamp}}
            </div>
            <div class="col">
                {{this.vallue}}
            </div>
            <div class="col">
                {{summa.note}}
            </div>
            <div class="col">
                <button @click="dosomething" class="btn btn-primary btn-md">Edit</button>
            </div>
            <div class="col">
                <button @click="doesomething(summa.lid)" class="btn btn-danger btn-md">Delete</button> 
            </div>
        </div>
    <div v-show="visible" class="row" id="edit">
   <div class="col">
    timestamp:
            <input type="datetime-local" max="limit" v-model="timestamp">
                </div>
    <div class="col">
    value:
<div v-if="s.types=='numerical'">
            <input type="number" v-model="value">
        </div>
        <div v-if="s.types=='boolean'">
            <input type="radio" v-model="value" value="true">true
            <input type="radio" v-model="value" value="false">false
        </div>
        <div v-if="s.types=='multichoice'">
            <select v-model="value"  >
            <option :value="i" v-for="i in op" >{{i}}</option>
            </select>
            <!-- <input type="text" v-model="tracker_type"> -->
        </div>
        <div v-if="s.types=='timeduration'">
            <input type="time" v-model="value">
        </div>
    </div>
 <div class="col">
     note
     <input type="text" v-model="note">
</div>
                 <div class="col">
           <button @click="backcall(summa.lid,event)" class="btn btn-success btn-md">submit</button>
                </div>
</div>
    </div>
</div>           
</template>

<script>
import store from '@/store';
export default {
    name:"logdisplay",
    data() {
        return {
            timestamp:"",
            value:this.summa.value,
            note:this.summa.note,
            s:store.state.currenttracker,
        op:store.state.currenttracker.settings.split(";"),
        }
    },
    computed:{
    minval:function(){
        let s= this.value.split(":")
        return (Number.parseInt(s[0])*60)+Number.parseInt(s[1])
    },
    limit:function(){
        return new Date();
    },
        finaltime:function(){
            try{
                let midddate= new Date(this.timestamp)
            console.log(midddate.getTime())
            return (midddate.getTime()/1000)
            }
            catch{
                return ""
            }
        },
        vallue:function(){
            console.log(this.summa.types)
            console.log(this.summa)
            console.log("printing")
            if (this.s.types=="timeduration"){
                let t= Number.parseInt(this.summa.value)
        let s= t%60
        let m= parseInt(t/60)
        let format= m.toString()+"h "+s.toString()+"m"
        return format
            }
            else{
                return this.summa.value
            }
        }
},
    props:["summa","visible"],
    methods: {
        dosomething:function(){
           if (this.visible===true){
                this.visible=false;
            }
            else{
                this.visible=true;
                
            }
        },
        backcall: async function(id,event){
console.log("i am called");
    var ts= sessionStorage.getItem("token")
    if (ts==null){
        window.alert("no hacking")
        this.$router.push("/one")
    }
    let val=""
    console.log(this.timestamp)
    
    if(this.value=="" || this.timestamp=="" || this.note=="" ){
        alert("please fill the details")
        return
    }

if (this.s.types=="timeduration"){
                this.value=this.minval
            }

   
    if(this.timestamp==""){
        var t= await fetch(this.$hostname+"logcrud/"+id,{
                    method:"PUT",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                      },
                    body:JSON.stringify({"value":this.value,"note":this.note,"timestamp":this.finaltime})
                });
                console.log(t)
                var ans= await t.json()
                
                this.visible=false
                this.$emit("refresh")
    }
    else{
    var t= await fetch(this.$hostname+"logcrud/"+id,{
                    method:"PUT",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + ts,
                      },
                    body:JSON.stringify({"value":this.value,"note":this.note,"timestamp":this.finaltime})
                });
                console.log(t)
                var ans= await t.json()
                
                this.visible=false
                this.$emit("refresh")
               
            } 
        },
            doesomething:async function(t_id){
    // alert("i am called for doesomething")
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
                console.log("calling refresh")
                this.$emit("refresh")
}
    },
}
</script>


<style scoped>
#one{
    margin-bottom: 20px;
}
#edit{
    margin-bottom: 20px;
}
</style>