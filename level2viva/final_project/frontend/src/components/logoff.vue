<script>
export default {
    name:"logoff",
    mounted() {
        sessionStorage.removeItem("token")
        this.$router.push("/one")
    },
}
</script>