<template>
    <div>
        <GChart :type=this.charttype :options="this.options" :data="this.chartdata" />
    </div>
</template>

<script>
import store from '@/store';
import {GChart} from "vue-google-charts/legacy"
export default {
    name:"customchart",
    components:{
        GChart
    },
    props:["type","data"],
    data:function(){
    return{
        options:{
             hAxis: { textPosition: 'none' },
             height:500,
             curveType:"function",
             backgroundColor:{fill:'transparent'}
        }
    }
},
computed:{
    charttype: function(){
        if (this.type=="numerical" || this.type=="timeduration"){
            return "LineChart"
    }
    else{
        return "PieChart"
    }
    },
    chartdata: function(){
        let charlist=[]
        if (this.type=="numerical"){
        
        console.log(this.charttype)
        charlist.push(["Timestamp","value"])
    this.data.forEach(element => {
        charlist.push([element.timestamp,Number.parseInt(element.value)])
        console.log("s..................../..................")
        console.log(Number.parseInt(element.value))
    });
    return charlist
    }
    else if (this.type=="boolean"){
        console.log("egw//////wt3ge//")
        console.log(this.charttype)
       let charlist=[]
        charlist.push(["value","count"])
        let al={
            true:0,
            false:0
        }
        console.log(this.data)
        this.data.forEach(element => {
            console.log(element.value)
            if (element.value=="true"){
                al.true+=1
            }
            else{
                al.false+=1
            }
        }
        )
        charlist.push(["true",al.true],["false",al.false])
        console.log(charlist)
        return charlist
    }
    else if (this.type=="timeduration"){
        
        console.log(this.charttype)
        charlist.push(["Timestamp","value"])
    this.data.forEach(element => {
        let t= Number.parseInt(element.value)
        let s= t%60
        let m= parseInt(t/60)
        let format= m.toString()+"h"+s.toString()+"m"
        charlist.push([element.timestamp,{v:t,f:format}])
        console.log("s..................../..................")
        console.log(Number.parseInt(element.value))
    });
    return charlist
    }
    else{
        let ans=[]
        let charlist={}
        ans.push(["value","count"])
        let s= store.state.currenttracker.settings.split(";")
        for(let i in s){
            charlist[s[i]]=0
        }
        console.log(charlist)
        this.data.forEach(element => {
            console.log(element.value)
            charlist[element.value]+=1
        })
        for(let i in s){
            ans.push([s[i],charlist[s[i]]])
        }

        return ans

    }
    }
}, 
}
</script>

