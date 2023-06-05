<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="successful_orders_list" icon="mdi-format-list-text"
                 label="سفارشات موفق"/>
          <q-tab class="text-primary" name="failed_orders_list" icon="mdi-format-list-text"
                 label="سفارشات ناموفق"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="successful_orders_list">
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
                    <q-td key="user">{{ props.row.user ? props.row.user.username : '-' }}</q-td>
                    <q-td key="product">{{ props.row.product ? props.row.product.title : '-' }}</q-td>
                    <q-td key="amount">{{ props.row.product ? props.row.product.price : '-' }}</q-td>
                    <q-td key="payment">{{ props.row.payment ? props.row.payment.ref_code : '-' }}</q-td>
                    <q-td key="size">{{ props.row.size ? props.row.size.title : '-' }}</q-td>
                    <q-td key="color">{{ props.row.color ? props.row.color.name : '-' }}</q-td>
                    <q-td key="count">{{ props.row.count }}</q-td>
                    <q-td key="payment_type">
                      <q-badge outline :color="ShowPaymentTypeColor(props.row.payment_type)"
                               :label="ShowPaymentType(props.row.payment_type)"/>
                    </q-td>
                    <q-td key="status">
                      <q-badge outline :color="ShowStatusTypeColor(props.row.status)"
                               :label="ShowStatus(props.row.status)"/>
                    </q-td>
                    <q-td key="name">{{ props.row.name }}</q-td>
                    <q-td key="family">{{ props.row.family }}</q-td>
                    <q-td key="phone">{{ props.row.phone }}</q-td>
                    <q-td key="address1">{{ props.row.address1 }}</q-td>
                    <q-td key="post_code">{{ props.row.post_code }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                  </q-tr>
                </template>
              </q-table>

              <div class="row justify-center q-mt-md" style="direction: ltr">
                <q-pagination v-model="paginationPage" color="teal" :max="lastPage" :max-pages="6"
                              :boundary-numbers="true" size="sm"/>
              </div>

            </div>
          </q-tab-panel>

          <q-tab-panel name="failed_orders_list">
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
                    <q-td key="product">{{ props.row.product ? props.row.product.title : '-' }}</q-td>
                    <q-td key="amount">{{ props.row.product ? props.row.product.price : '-' }}</q-td>
                    <q-td key="payment">{{ props.row.payment ? props.row.payment.ref_code : '-' }}</q-td>
                    <q-td key="size">{{ props.row.size ? props.row.size.title : '-' }}</q-td>
                    <q-td key="color">{{ props.row.color ? props.row.color.name : '-' }}</q-td>
                    <q-td key="count">{{ props.row.count }}</q-td>
                    <q-td key="payment_type">
                      <q-badge outline :color="ShowPaymentTypeColor(props.row.payment_type)"
                               :label="ShowPaymentType(props.row.payment_type)"/>
                    </q-td>
                    <q-td key="status">
                      <q-badge outline :color="ShowStatusTypeColor(props.row.status)"
                               :label="ShowStatus(props.row.status)"/>
                    </q-td>
                    <q-td key="name">{{ props.row.name }}</q-td>
                    <q-td key="family">{{ props.row.family }}</q-td>
                    <q-td key="phone">{{ props.row.phone }}</q-td>
                    <q-td key="address1">{{ props.row.address1 }}</q-td>
                    <q-td key="post_code">{{ props.row.post_code }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
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
          name: 'amount',
          align: 'left',
          label: 'مبلغ',
          field: 'amount',
          sortable: true
        },
        {
          name: 'payment',
          align: 'left',
          label: 'پرداختی',
          field: 'payment',
          sortable: true
        },
        {
          name: 'size',
          align: 'left',
          label: 'سایز',
          field: 'size',
          sortable: true
        },
        {
          name: 'color',
          align: 'left',
          label: 'رنگ',
          field: 'color',
          sortable: true
        },
        {
          name: 'count',
          align: 'left',
          label: 'تعداد',
          field: 'count',
          sortable: true
        },
        {
          name: 'payment_type',
          align: 'left',
          label: 'نوع پرداخت',
          field: 'payment_type',
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
          name: 'name',
          align: 'left',
          label: 'نام',
          field: 'name',
          sortable: true
        },
        {
          name: 'family',
          align: 'left',
          label: 'نام خانوادگی',
          field: 'family',
          sortable: true
        },
        {
          name: 'phone',
          align: 'left',
          label: 'موبایل',
          field: 'phone',
          sortable: true
        },
        {
          name: 'address1',
          align: 'left',
          label: 'آدرس 1',
          field: 'address1',
          sortable: true
        },
        {
          name: 'post_code',
          align: 'left',
          label: 'آدرس 2',
          field: 'post_code',
          sortable: true
        },
        {
          name: 'created_at',
          align: 'left',
          label: 'تاریخ ثبت',
          field: 'created_at',
          sortable: true
        }
      ],

      tab: 'successful_orders_list',
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
    ShowPaymentType (type) {
      if (type === 'online') {
        return 'آنلاین'
      }
      return 'نقدی (حضوری)'
    },

    ShowPaymentTypeColor (type) {
      if (type === 'online') {
        return 'orange'
      }

      return 'red'
    },

    ShowStatus (type) {
      if (type === 'sending') {
        return 'درحال ارسال'
      } else if (type === 'posted') {
        return 'ارسال شده'
      }
      return 'دریافت شده'
    },

    ShowStatusTypeColor (type) {
      if (type === 'sending') {
        return 'red'
      } else if (type === 'posted') {
        return 'orange'
      }

      return 'secondary'
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

    GetAllSuccessfulOrders () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/panel/orders/success/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    },

    GetAllUnSuccessfulOrders () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/panel/orders/fail/?page=' + app.paginationPage + '&search=' + app.search)
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
      if (this.tab === 'successful_orders_list') {
        this.GetAllSuccessfulOrders()
      } else {
        this.GetAllUnSuccessfulOrders()
      }
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      if (this.tab === 'successful_orders_list') {
        this.GetAllSuccessfulOrders()
      } else {
        this.GetAllUnSuccessfulOrders()
      }
    },

    tab (value) {
      this.paginationPage = 1

      if (value === 'successful_orders_list') {
        this.request_type = 'successful'
        this.GetAllSuccessfulOrders()
      } else {
        this.request_type = 'failed_orders_list'
        this.GetAllUnSuccessfulOrders()
      }
    }
  },

  mounted () {
    this.GetAllSuccessfulOrders()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
