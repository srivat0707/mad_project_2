
<template>
<div class="d-flex  justify-content-center">
<div id="form" class="d-flex flex-column" >
    <div class="card bgforrow">
        <div class="card-body">
<div class="first">
        <label class="label" id ="label1">username:</label>
        <input type="text" name="username" maxlength="20" required id="user_name" autocomplete="off" autofocus  v-model="Username"/>
    </div>
    <div class="first">
        <label class="label" id="label2">password:</label>
        <input type="password" name="password"  id="pass_word" maxlength="20" autocomplete="off" required v-model="Password"/>
    </div>
    <div class="first">
        <label class="label" id ="label1">email:</label>
        <input type="email" v-model="email"/>
        <!-- <input type="" name="username" maxlength="20" required id="user_name" autocomplete="off" autofocus  v-model="Username"/> -->
    </div>
    <div class="send">
        <a  class="btn btn-primary btn-md"  @click="submitting" role="button" >Signup</a>
      </div>
        </div>
    </div>
<div>
</div>
    


</div>
</div>
    
    
</template>

<style scoped >
.form-group{
    margin: 5%;
}
.sbbt{
    padding-left: 20%;
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
/* #app{
    color: transparent;
} */
 #form{margin-top: 10%;width: 436px;height: 300px;}label{font-size: 1.8em;}h1{margin-top: 40px;text-align: center;}input{margin-left: 5%;padding: 8px;font-size: 1.5em;border-radius: 20px;background-color: rgba(255, 255, 255, 0.055);}#button{margin-left: 25;font-size: 1.4em;}
</style>

<script>
export default {
    name:"loginform",
    data:function(){
        return{
        Username:"",
        Password:"",
        email:""
        }
    },
    methods:{
        submitting:async function(event){
            console.log("i am called");
            console.log(event);
            try {
                var t= await fetch(this.$hostname+"newuser",{
                    method:"POST",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json'
                      },
                    body:JSON.stringify({"username":this.Username,"password":this.Password,"email":this.email})
                });
                var ans= await t.json()
                if(!t.ok){
                    alert(ans.message)
                }else{
                    sessionStorage.setItem("token",ans.token);
                    sessionStorage.setItem("name",this.Username);
                    this.$router.replace("/three")

                }
            } catch (error) {
                console.log(error)
                console.log("oops");
                window.alert(error)  
            }
            
           
            
        }
    }
}
</script>