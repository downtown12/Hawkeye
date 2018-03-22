<template>
  <div class="setting-card">
    <p>勾选要导出的扫描任务标签/关键词，然后点击导出开始导出报告：</p>
    <span v-for="item in statistics"> 
      <input type="checkbox" :id="item._id" :value="item._id" v-model="checkedTags">
        <label :for="item._id">{{item._id}}</label>
    </span>
      <br>
      <span>要导出的关键词: {{ checkedTags | json }}</span>
      <el-button style="float: right;" type="info" @click="dialogConfirmVisible = true">导出
      </el-button>

      <el-dialog title="确认" v-model="dialogConfirmVisible">
        <p>确认要将以下关键词导出导报告</p>
        <p>{{checkedTags}}</p>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogConfirmVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleCreateKeywordReport(checkedTags)">确 定</el-button>
        </div>
      </el-dialog>
  </div>

</template>

<script>
  require("babel-polyfill");
  export default {
    data() {
      return {
        activeIndex: '1',
        statistics: [],
        //test data
        //statistics: [{'_id':'直销银行'}, {'_id':'CPOS'}],
        checkedTags: [],
        dialogConfirmVisible: false,
        report : ''
      }
    }, methods: {
      fetchStatisticsData() {
        this.axios.get(`${this.GLOBAL.statistics}`)
          .then((response) => {
            this.statistics = response.data.result;

          })
          .catch((error) => {
            this.$message.error(error.toString());
          });
      },
      async handleCreateKeywordReport(checkedTags) {
          try{
            let response = await this.axios.get(`${this.GLOBAL.keywordReport}/${checkedTags}`, {responseType: 'blob'})
            this.dialogConfirmVisible = false;
            let disposition = response.headers['content-disposition']
            let filename = decodeURI(disposition.match(/filename="(.*)"/)[1]);
            this.fileDownload(response.data, filename);
          }
          catch(error) {
            this.$message.error(error.toString());
            this.dialogConfirmVisible = false;
          };
      }
    },
    mounted: function () {
      this.fetchStatisticsData();
      this.$nextTick(function () {
      });
    }
  }
</script>
