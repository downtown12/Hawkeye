<template>
  <el-tabs active-name="keywordreport">
    <el-tab-pane name="keywordreport">
      <span slot="label"><i class="el-icon-edit"></i> 按关键词导出</span>
      <KeywordReport></KeywordReport>
    </el-tab-pane>

    <el-tab-pane name="periodreport">
      <span slot="label"><i class="el-icon-menu"></i> 按时间导出</span>
      <PeriodReport></PeriodReport>

    </el-tab-pane>
    <el-tab-pane name="taskreport">
      <span slot="label"><i class="el-icon-message"></i> 按巡检任务导出</span>
      <TaskReport></TaskReport>

    </el-tab-pane>
  </el-tabs>

</template>

<script>
  import KeywordReport from './KeywordReport';
  import PeriodReport from './PeriodReport';
  import TaskReport from './TaskReport';

  export default {
    components:  {
      KeywordReport,
      PeriodReport,
      TaskReport
    },
  }

</script>

<style>
  .tip a {
    text-decoration: none;
    line-height: 36px;
  }

  .item {
    padding: 5px 0;
    margin-left: 10px;
    margin-right: 10px;
  }

  .item .el-tag {
    margin-top: 5px;
    margin-left: 10px;
    margin-right: 10px;
  }
</style>
