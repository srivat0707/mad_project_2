<template>
  <div id="app">
        <router-view :key="$route.fullPath" ></router-view>
        
                <!-- <div>
            <div>
                <input type="text">
            </div>
            <div>
                <input type="button" @click="submit">
            </div>
        </div> -->
    </div>
</template>

