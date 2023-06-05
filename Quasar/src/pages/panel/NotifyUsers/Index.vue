<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="notifyusers_list" icon="mdi-format-list-text"
                 label="اطلاع رسانی ها"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="notifyusers_list">
            <q-input style="max-width: 300px !important;"
                     dense v-model.lazy="search"
                     debounce="250"
                     filled type="search">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>
            <div class="q-pa-md">
              <q-table
                :data="data"
                :columns="columns"
                :loading="loading"
                row-key="id"
                :rows-per-page-options="[10]"
                binary-state-sort
                flat
                separator="horizontal"
                color="brand"
              >
                <template v-slot:body="props">
                  <q-tr :props="props">
                    <q-td key="id">{{ props.rowIndex + 1 }}</q-td>
                    <q-td key="product">{{ props.row.product.title }}</q-td>
                    <q-td key="original_image">
                      <q-img
                        :src="ShowImage(props.row.product.original_image)"
                        spinner-color="white"
                        style="height: 80px; max-width: 60px"
                      />
                    </q-td>
                    <q-td key="status">
                      <q-badge outline :color="ShowStatusTypeColor(props.row.active)"
                               :label="ShowStatus(props.row.active)"/>
                    </q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="DeleteUserNotify(props.row.user.username + '-' +  props.row.product.title , props.row.id)"
                        style="color: red" rounded
                        icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn
                        @click="ChangeNotifyUserStatus(props.row.user.username + '-' +  props.row.product.title , props.row.id , props.row.active)"
                        :style="props.row.active ? {'color' : 'red'} : {'color' : 'green'}" rounded
                        :icon="props.row.active ?  'mdi-close-outline' : 'mdi-shield-check-outline'" :label="props.row.active ?  'منقضی بشه' : 'دوباره فعال بشه'" size="md" flat dense>
                        <q-tooltip>{{ props.row.active ?  'دوباره فعال بشه' : 'منقضی بشه' }}</q-tooltip>

                      </q-btn>
                    </q-td>
                  </q-tr>
                </template>
              </q-table>

              <div class="row justify-center q-mt-md" style="direction: ltr">
                <q-pagination v-model="paginationPage" color="teal" :max="lastPage" :max-pages="6"
                              :boundary-numbers="true" size="sm"/>
              </div>

            </div>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </div>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  data () {
    return {
      search: '',

      data: [],

      paginationPage: 1,
      lastPage: 0,
      pages_count: 0,

      loading: false,
      columns: [
        {
          name: 'id',
          required: true,
          label: 'ردیف',
          align: 'left',
          field: row => row.name,
          sortable: true
        },
        {
          name: 'product',
          align: 'left',
          label: 'محصول',
          field: 'product',
          sortable: true
        },
        {
          name: 'original_image',
          align: 'left',
          label: 'عکس محصول',
          field: 'original_image',
          sortable: true
        },
        {
          name: 'status',
          align: 'left',
          label: 'وضعیت',
          field: 'status',
          sortable: true
        },
        {
          name: 'created_at',
          align: 'left',
          label: 'تاریخ ثبت',
          field: 'created_at',
          sortable: true
        },
        {
          name: 'setting',
          align: 'left',
          label: 'عملیات',
          field: 'setting',
          sortable: true
        }
      ],

      tab: 'notifyusers_list',
      splitterModel: 20,
      showDialog: false
    }
  },

  filters: {
    FormatDate (date) {
      return moment(date).format('HH:mm  YYYY-MM-DD')
    }
  },

  methods: {
    ShowImage (url) {
      return url.replace('http://localhost:8000/', process.env.api)
    },

    ShowStatus (type) {
      if (type) {
        return 'فعال'
      }
      return 'منقضی'
    },

    ShowStatusTypeColor (type) {
      if (type) {
        return 'secondary'
      }
      return 'red'
    },

    ChangeNotifyUserStatus (title, id, currentActive) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت تایید اطلاع رسانی ' + ' ( ' + title + ' ) ' + 'نقض شود ؟ ',
        ok: {
          push: true,
          label: 'تایید'
        },
        cancel: {
          push: true,
          color: 'negative'
        },
        persistent: true
      }).onOk(() => {
        const formData = new FormData()
        formData.append('active', !currentActive)

        app.$axios.put(process.env.api + 'api/panel/notify_users/' + id + '/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllUserNotifies()
            }
            if (currentActive) {
              app.showNotif('اطلاع رسانی مورد نظر با موفقیت غیر فعال شد', 'mdi-checkbox-marked-circle-outline', 'green')
            } else {
              app.showNotif('اطلاع رسانی مورد نظر با موفقیت فعال شد', 'mdi-checkbox-marked-circle-outline', 'green')
            }
          })
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

    DeleteUserNotify (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید اطلاع رسانی ' + ' ( ' + name + ' ) ' + 'برای همیشه حذف شود ؟ ',
        ok: {
          push: true,
          label: 'تایید'
        },
        cancel: {
          push: true,
          color: 'negative'
        },
        persistent: true
      }).onOk(() => {
        app.$axios.delete(process.env.api + 'api/panel/notify_users/' + id)
          .then(function () {
            app.showNotif('اطلاع رسانی مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllUserNotifies()
            }
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    GetAllUserNotifies () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/panel/notify_users/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    }
  },

  watch: {
    search () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      this.GetAllUserNotifies()
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      this.GetAllUserNotifies()
    }
  },

  mounted () {
    this.GetAllUserNotifies()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
