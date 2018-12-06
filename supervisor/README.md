## 实现通过event监控进程异常退出发送邮件报警

自定义eventlistener， 接收 PROCESS_STATE_EXITED 事件，并触发邮件报警
