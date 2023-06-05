<template>
  <div>

  </div>
</template>

<script>

function getCookie (name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

export default {
  mounted () {
    this.isLogin()
  },

  methods: {
    showNotif (message, icon = 'error', color = 'red') {
      this.$q.notify({
        message: message,
        icon: icon,
        color: color,
        position: 'bottom-left',
        progress: true
      })
    },

    isLogin () {
      const app = this

      this.$axios.post(process.env.api + 'api/auth/isLogin/')
        .then(function (response) {
          if (response.data.login_status && response.data.super_user_status) {
            app.$router.push('/panel/user')
          }
          app.Logout()
        })
        .catch(function () {
          localStorage.removeItem('token')
          delete app.$axios.defaults.headers.common.Authorization
          app.$q.loading.hide()
        })
    },

    Logout () {
      const app = this

      const csrftoken = getCookie('csrftoken')

      this.$q.loading.show()
      this.$axios.post(process.env.api + 'api/auth/logout/', {}, {
        withCredentials: true,
        headers: { 'X-CSRFToken': csrftoken }
      })
        .then(function () {
          localStorage.removeItem('token')
          delete app.$axios.defaults.headers.common.Authorization

          window.location.href = process.env.api
        })
        .finally(function () {
          app.$q.loading.hide()
        })
    }
  }
}
</script>
