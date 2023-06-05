<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن کیف پول</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> مبلغ (به تومان) <span class="text-red"
                                                            style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.amount"
                     dense/>
          </div>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.user" map-options
                      lazy-rules
                      required
                      :options="users_list" option-value="id"
                      option-label="username" label="کاربر*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.status" map-options :options="types_list" option-value="value"
                      option-label="key" label="وضعیت*"/>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش کیف پول': 'ثبت کیف پول'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'users_list'],

  data () {
    return {
      types_list: [
        {
          key: 'فعال',
          value: true
        },
        {
          key: 'غیر فعال',
          value: false
        }
      ]
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (this.form.amount === undefined || this.form.amount === '') {
        this.showNotif('فیلد مبلغ اجباری است')
        return
      }

      if (!this.form.user || this.form.user.id === 0) {
        app.showNotif('فیلد کاربر الزامی است')
        return
      }

      if (!this.form.user || this.form.user.id === 0) {
        this.form.user_id = null
      } else {
        this.form.user_id = this.form.user.id
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      if (this.form.status && this.form.status.value !== undefined) {
        formData.append('status', this.form.status.value)
      } else {
        formData.append('status', true)
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateWallet(app, formData)
      } else {
        this.UpdateWallet(app, formData)
      }
    },

    CreateWallet (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/wallets/', formData)
        .then(function () {
          app.showNotif('کیف پول مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllWallets()
          app.$parent.$parent.GetRequiredList()
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    UpdateWallet (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/wallets/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('کیف پول مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllWallets()
          app.$parent.$parent.GetRequiredList()
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    showNotif (message, icon = 'error', color = 'red') {
      this.$q.notify({
        message: message,
        icon: icon,
        color: color,
        position: 'bottom-right',
        progress: true
      })
    }
  },

  computed: {
    _dialog: {
      get () {
        return this.showDialog
      },
      set (value) {
        this.$emit('update:showDialog', value)
      }
    }
  }
}
</script>
