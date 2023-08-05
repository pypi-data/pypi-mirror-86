### dup

* dup主要utx的修改，对由python3.5的支持转换为python2.7
    * 支持Python2.7


* 安装dup  

    ```
    pip install dup
    ```

* 功能列表
    * 用例排序，只需要导入dup库，用例的执行顺序就会和编写顺序一致
    * 用例自定义标签，可以对测试用例指定多个标签。
    目前全部用例默认带有`FULL`标签，未指定标签的用例，默认带有`SMOKE`和`FULL`两个标签。

* 示例

    ```py
    @unique
    class Tag(Enum):
        SMOKE = 1  # 冒烟测试标记，可以重命名，但是不要删除
        FULL = 1000  # 完整测试标记，可以重命名，但是不要删除

        # 以下开始为扩展标签，自行调整
        SP = 2
    ```

    ```py
    class TestLegion(unittest.TestCase):

        @tag(Tag.SMOKE)
        def test_create_legion(self):
            pass

        @tag(Tag.SP, Tag.FULL)
        def test_quit_legion(self):
            """退出军团

            :return:
            """
            print("吧啦啦啦啦啦啦")
            assert 1 == 2
    ```

* 运行指定标签的测试用例

    ```py
    from dup import *

    if __name__ == '__main__':
        setting.run_case = {Tag.SMOKE}  # 只运行SMOKE冒烟用例
        runner = TestRunner()
        runner.add_case_dir(r"testcase")
        runner.run_test(report_title='接口自动化测试报告')
    ```

* 数据驱动  

    ```py
    class TestLegion(unittest.TestCase):

        @data(["gold", 100], ["diamond", 500])
        def test_bless(self, bless_type, award):
            print(bless_type)
            print(award)

        @data(10001, 10002, 10003)
        def test_receive_bless_box(self, box_id):
            """ 领取祈福宝箱

            :return:
            """
            print(box_id)

* 默认会解包测试数据来一一对应函数参数，可以使用unpack=False，不进行解包  

	```py
	class TestBattle(unittest.TestCase):
	    @data({"gold": 1000, "diamond": 100}, {"gold": 2000, "diamond": 200}, unpack=False)
	    def test_get_battle_reward(self, reward):
	        """ 领取战斗奖励
	
	        :return:
	        """
	        print(reward)
	        print("获得的钻石数量是：{}".format(reward['diamond']))
	 ```

* 检测用例是否编写了用例描述  

    ```
    2017-11-13 12:00:19,334 WARNING legion.test_legion.test_bless没有用例描述
    ```

* 执行测试时，显示测试进度  

    ```
    2017-11-13 12:00:19,336 INFO 开始进行测试
	2017-11-13 12:00:19,436 INFO Start to test legion.test_legion.test_create_legion (1/5)
	2017-11-13 12:00:19,536 INFO Start to test legion.test_legion.test_receive_bless_box (2/5)
	2017-11-13 12:00:19,637 INFO Start to test legion.test_legion.test_receive_bless_box (3/5)
	2017-11-13 12:00:19,737 INFO Start to test legion.test_legion.test_receive_bless_box (4/5)
	2017-11-13 12:00:19,837 INFO Start to test legion.test_legion.test_quit_legion (5/5)
    ```

* setting类提供多个设置选项进行配置  

    ```py
    class setting:

        # 只运行的用例类型
        run_case = {Tag.SMOKE}

        # 开启用例排序
        sort_case = True

        # 每个用例的执行间隔，单位是秒
        execute_interval = 0.1

        # 开启检测用例描述
        check_case_doc = True

        # 显示完整用例名字（函数名字+参数信息）
        full_case_name = False

        # 测试报告显示的用例名字最大程度
        max_case_name_len = 80

        # 执行用例的时候，显示报错信息
        show_error_traceback = True

        # 生成ztest风格的报告
        create_ztest_style_report = True

        # 生成bstest风格的报告
        create_bstest_style_report = True
    ```

* 集成 [ztest](https://github.com/zhangfei19841004/ztest) 和 [BSTestRunner](https://github.com/easonhan007/HTMLTestRunner) 自动生成两份测试报告，感谢两位作者的测试报告模版

* ztest风格

  ![ztest风格](https://github.com/jianbing/utx/raw/master/img/ztest.png)

* bstest风格

  ![bstest风格](https://github.com/jianbing/utx/raw/master/img/bstest.png)

* 无缝接入unittest项目，导入utx包即可开始使用扩展功能，无需修改之前的代码

## 更新 1.1.1:

   去除 跳过用例数，增加用例程序错误数

## 更新1.1.2:

   更新内容:

      1、修复展示文本溢出无法收缩的问题
      2、case 增加报告负责人列（需要在 case 类文件注释里  增加【xx】 xx 【】为中文符号 代表 case 负责人 ）

## 更新1.1.3:

    更新内容:

    run方法增加返回值

## 更新1.1.4:
    更新内容： case 返回 unittest 用例名，去除 _
    
## 更新1.1.5:
    更新内容： case 执行时间返回格式改为秒级别
    
## 更新1.1.6:
    更新内容：失败case 或者 错误case 增加case 层面的重试。
    runner = TestRunner()
    runner.run_test() 方法增加可选参数： retry=0 （重试次数）

## 更新1.1.7:
    更新内容：多进程执行自动化时，有偶现的报错，当前版本fix了该问题。