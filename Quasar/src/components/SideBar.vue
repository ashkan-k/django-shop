<template>
  <div v-if="$store.state.shop.user">
    <q-item to="/user/dashboard" class="item-side-bar"
            active-class="q-item-no-link-highlighting">
      <q-item-section avatar>
        <q-icon name="dashboard"/>
      </q-item-section>
      <q-item-section>
        <q-item-label>داشبورد</q-item-label>
      </q-item-section>
    </q-item>

    <q-item to="/user/profile" class="item-side-bar" active-class="item-side-bar-active">
      <q-item-section avatar>
        <q-icon name="mdi-account-circle"/>
      </q-item-section>
      <q-item-section>
        <q-item-label>پروفایل</q-item-label>
      </q-item-section>
    </q-item>

    <!--    ############################################################################-->

    <div v-if="CanSeeSidebarItems()">
      <q-item to="/user/carts" class="item-side-bar" active-class="item-side-bar-active">
        <q-item-section avatar>
          <q-icon name="mdi-cart"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>سبد خرید</q-item-label>
        </q-item-section>
      </q-item>
      <q-item to="/user/orders" class="item-side-bar" active-class="item-side-bar-active">
        <q-item-section avatar>
          <q-icon name="mdi-shopping"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>سفارشات</q-item-label>
        </q-item-section>
      </q-item>
      <q-item to="/user/wishlists" class="item-side-bar" active-class="item-side-bar-active">
        <q-item-section avatar>
          <q-icon name="mdi-bookmark-multiple"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>علاقه مندی ها</q-item-label>
        </q-item-section>
      </q-item>
      <q-item to="/user/notify_users" class="item-side-bar" active-class="item-side-bar-active">
        <q-item-section avatar>
          <q-icon name="mdi-phone-message"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>اطلاع رسانی ها</q-item-label>
        </q-item-section>
      </q-item>
      <q-item to="/user/stars" class="item-side-bar" active-class="item-side-bar-active">
        <q-item-section avatar>
          <q-icon name="mdi-star-half-full"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>امتیاز شما به محصولات</q-item-label>
        </q-item-section>
      </q-item>
      <q-item to="/user/comments" class="item-side-bar" active-class="item-side-bar-active">
        <q-item-section avatar>
          <q-icon name="mdi-comment-processing"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>نظرات</q-item-label>
        </q-item-section>
      </q-item>
      <q-item to="/user/coupons" class="item-side-bar" active-class="item-side-bar-active">
        <q-item-section avatar>
          <q-icon name="mdi-percent"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>کد های تخفیف</q-item-label>
        </q-item-section>
      </q-item>
      <q-item to="/user/tickets" class="item-side-bar" active-class="item-side-bar-active">
        <q-item-section avatar>
          <q-icon name="mdi-ticket-percent-outline"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>تیکت ها</q-item-label>
        </q-item-section>
      </q-item>

      <q-item to="/user/wallet" class="item-side-bar" active-class="item-side-bar-active">
        <q-item-section avatar>
          <q-icon name="mdi-wallet"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>کیف پول</q-item-label>
        </q-item-section>
      </q-item>

      <div v-if="CheckIsSupporter()">
        <q-separator inset="true" class="q-my-sm"/>
        <q-expansion-item
          class="item-side-bar"
          icon="mdi-server-security"
          label="وظایف مدیریتی"
        >

          <q-list style="border-radius: 15px">
            <q-item to="/user/user_tickets" class="item-side-bar"
                    active-class="item-side-bar-active">
              <q-item-section avatar>
                <q-icon name="mdi-ticket-percent-outline"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>تیکت های کاربران</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-expansion-item>
      </div>
    </div>

    <!--    ################################################################################-->

    <div v-else>
      <div v-if="$store.state.shop.user.is_superuser">
        <q-item to="/admin/categories" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-menu"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>دسته بندی ها</q-item-label>
          </q-item-section>
        </q-item>

        <q-item v-if="$store.state.shop.user.is_superuser || CheckIsAuthor()" to="/admin/articles"
                class="item-side-bar"
                active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-newspaper-variant-outline"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>مقالات</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/products" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-newspaper"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>محصولات</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/colors" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-format-color-fill"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>رنگ ها</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/sizes" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-size-xxs"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>سایزها</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/images" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-image"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>گالری تصاویر</q-item-label>
          </q-item-section>
        </q-item>

        <q-expansion-item
          class="item-side-bar"
          icon="perm_identity"
          label="کاربران"
        >

          <q-list style="border-radius: 15px">

            <q-item to="/admin/users" class="item-side-bar" active-class="item-side-bar-active">
              <q-item-section avatar>
                <q-icon name="mdi-account"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>لیست کاربران</q-item-label>
              </q-item-section>
            </q-item>

            <q-item to="/admin/block_users" class="item-side-bar" active-class="item-side-bar-active">
              <q-item-section avatar>
                <q-icon name="mdi-account-circle"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>کاربران بلاک شده</q-item-label>
              </q-item-section>
            </q-item>

          </q-list>
        </q-expansion-item>

        <q-expansion-item
          class="item-side-bar"
          icon="mdi-server-security"
          label="سطح دسترسی"
        >

          <q-list style="border-radius: 15px">

            <q-item to="/admin/acl/roles" class="item-side-bar" active-class="item-side-bar-active">
              <q-item-section avatar>
                <q-icon name="mdi-ticket-account"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>لیست نقش ها</q-item-label>
              </q-item-section>
            </q-item>

            <q-item to="/admin/acl/permissions" class="item-side-bar" active-class="item-side-bar-active">
              <q-item-section avatar>
                <q-icon name="mdi-ticket-account"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>لیست دسترسی ها</q-item-label>
              </q-item-section>
            </q-item>

            <q-item to="/admin/acl/role_user" class="item-side-bar" active-class="item-side-bar-active">
              <q-item-section avatar>
                <q-icon name="mdi-ticket-account"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>نقش کاربری</q-item-label>
              </q-item-section>
            </q-item>

            <q-item to="/admin/acl/role_permission" class="item-side-bar" active-class="item-side-bar-active">
              <q-item-section avatar>
                <q-icon name="mdi-ticket-account"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>نقش دسترسی</q-item-label>
              </q-item-section>
            </q-item>

          </q-list>
        </q-expansion-item>

        <q-item to="/admin/carts" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-cart"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>سبد خرید</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/coupons" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-percent"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>کد تخفیف</q-item-label>
          </q-item-section>
        </q-item>

        <q-expansion-item
          class="item-side-bar"
          icon="mdi-ticket"
          label="تیکت ها"
        >

          <q-list style="border-radius: 15px">

            <q-item to="/admin/tickets" class="item-side-bar" active-class="item-side-bar-active">
              <q-item-section avatar>
                <q-icon name="mdi-ticket-percent-outline"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>لیست تیکت ها</q-item-label>
              </q-item-section>
            </q-item>

            <q-item to="/admin/tickets/questions" class="item-side-bar" active-class="item-side-bar-active">
              <q-item-section avatar>
                <q-icon name="mdi-ticket-outline"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>سوال های تیکت ها</q-item-label>
              </q-item-section>
            </q-item>

            <q-item to="/admin/tickets/answers" class="item-side-bar" active-class="item-side-bar-active">
              <q-item-section avatar>
                <q-icon name="mdi-ticket-account"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>پاسخ های تیکت ها</q-item-label>
              </q-item-section>
            </q-item>

          </q-list>
        </q-expansion-item>

        <q-item to="/admin/wishlists" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-bookmark-multiple"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>علاقه مندی ها</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/wallets" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-wallet"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>کیف پول ها</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/sliders" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-dock-window"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>اسلایدر</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/comments" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-comment-processing"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>نظرات</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/likes_dislikes" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-heart-half-full"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>پسندیده | ناپسندیده</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/stars" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-star-half-full"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>امتیازت ها</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/notify_users" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-phone-message"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>اطلاع رسانی ها</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/orders" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-shopping"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>سفارشات</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/payments" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-wallet"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>پرداخت ها</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/newsletters" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-email-newsletter"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>خبرنامه ها</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/admin/settings" class="item-side-bar" active-class="item-side-bar-active">
          <q-item-section avatar>
            <q-icon name="mdi-cog"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>تنظیمات</q-item-label>
          </q-item-section>
        </q-item>
      </div>
    </div>

    <q-separator inset="true" class="q-my-sm"/>

    <q-item @click="Logout" class="item-side-bar hover_cursor" active-class="item-side-bar-active">
      <q-item-section avatar>
        <q-icon name="mdi-logout"/>
      </q-item-section>
      <q-item-section>
        <a @click="Logout()">
          <q-item-label>خروج</q-item-label>
        </a>
      </q-item-section>
    </q-item>

  </div>
</template>

<style>
.hover_cursor:hover {
  cursor: pointer;
  background-color: #dedcdc;
}
</style>

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
  name: 'SideBar',
  methods: {
    isLogin () {
      const app = this

      this.$axios.post(process.env.api + 'api/auth/isLogin/')
        .then(function (response) {
          if (!response.data.login_status) {
            app.$router.push('/login')
          }
          app.$store.commit('shop/setUser', response.data.user)
        })
        .catch(function () {
          app.$router.push('/login')
        })
        .finally(function () {
          app.$q.loading.hide()
        })
    },
    showNotif (message, icon = 'error', color = 'red', time = 3000) {
      this.$q.notify({
        message: message,
        icon: icon,
        color: color,
        position: 'bottom-right',
        timeout: time,
        progress: true
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

          app.showNotif('شما با موفقیت خارج شدید', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$router.push('/login')
        })
        .finally(function () {
          app.$q.loading.hide()
        })
    },

    CanSeeSidebarItems () {
      if (window.location.href.includes('panel/user')) {
        return true
      }
      return false
    },
    CheckIsAuthor () {
      const roles = this.$store.state.shop.user.roles
      if (roles) {
        const result = roles.filter(x => x.role.title === 'author')
        if (result.length > 0) {
          return true
        }
        return false
      }
      return false
    },

    CheckIsSupporter () {
      const roles = this.$store.state.shop.user.roles
      if (roles) {
        const result = roles.filter(x => x.role.title === 'supporter')
        if (result.length > 0) {
          return true
        }
      }
      return false
    }
  }
}
</script>
