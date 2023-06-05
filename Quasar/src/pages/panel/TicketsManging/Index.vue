<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="tickets_list" icon="mdi-format-list-text" label="تیکت های کاربران"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="tickets_list">
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
                    <q-td key="title">{{ props.row.title }}
                    </q-td>
                    <q-td key="questions_count">{{ props.row.questions_count }}</q-td>
                    <q-td key="answers_count">{{ props.row.answers_count }}</q-td>
                    <q-td key="status">
                      <q-badge outline :color="ShowStatusColor(props.row.status)"
                               :label="ShowStatus(props.row.status)"/>
                    </q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                    <q-btn
                        @click="$router.push('user_tickets/' + props.row.id)"
                        rounded
                        icon="mdi-comment-eye" label="نمایش" size="md" flat
                        dense>
                        <q-tooltip>نمایش</q-tooltip>
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
          name: 'title',
          align: 'left',
          label: 'عنوان',
          field: 'title',
          sortable: true
        },
        {
          name: 'questions_count',
          align: 'left',
          label: 'تعداد سوال ها',
          field: 'questions_count',
          sortable: true
        },
        {
          name: 'answers_count',
          align: 'left',
          label: 'تعداد پاسخ ها',
          field: 'answers_count',
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

      tab: 'tickets_list',
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
          app.CheckIsSupporter()
        })
    },

    CheckIsSupporter () {
      const roles = this.$store.state.shop.user.roles
      if (roles) {
        const result = roles.filter(x => x.role.title === 'supporter')
        if (result.length === 0) {
          window.location.href = '/'
        }
      } else {
        window.location.href = '/'
      }
    },

    ShowStatus (status) {
      if (status) {
        return 'باز'
      }
      return 'بسته'
    },

    ShowStatusColor (status) {
      if (status) {
        return 'secondary'
      }
      return 'red'
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

    GetAllTickets () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/panel/tickets/all_users/?page=' + app.paginationPage + '&search=' + app.search)
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
      this.GetAllTickets()
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      this.GetAllTickets()
    }
  },

  mounted () {
    this.isLogin()
    this.GetAllTickets()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
