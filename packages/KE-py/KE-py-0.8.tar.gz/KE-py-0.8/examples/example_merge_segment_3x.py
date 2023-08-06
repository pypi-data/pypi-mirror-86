# coding=u8
import sys
import traceback
from dateutil.relativedelta import relativedelta
from KE import KE
from KE.v3.segments import Segments
import time
from datetime import datetime, timedelta
import calendar
from KE.client import KE3CONF as CONF

client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=3)


# 获取当前日期
today = datetime.today().date()
# convert date to datetime
today = datetime.fromordinal(today.toordinal())

# 获取KE 的某个cube对象
cube1 = client.cubes(name='kylin_sales_cube')[0]


def merge_week_by_month(cube, year, month):
    """
    根据某月按周合并segment，如果出现夸月的segment则放弃合并
    :param cube:
    :param year:
    :param month:
    :return:
    """

    week_start_end_list = []

    # 构造某个月的start 日期
    start = datetime(year, month, 1, 0, 0)

    # 获取第一个星期一
    if start.weekday() != 0:
        start = start + timedelta(days=(7 - start.weekday()))

    for i in range(4):
        # end of a week
        end = start + timedelta(days=7)
        if end.month != month:
            # 已夸月
            break
        start_end = (start, end)
        week_start_end_list.append(start_end)

        start = end

    # 开始合并操作
    for start, end in week_start_end_list:
        # 获取segments对象
        segments = cube.segments(start_time=start, end_time=end, size=1000)

        # 检查下segments的个数
        seg_list = segments.list_segments()
        print('segment numbers %s' % len(seg_list))

        if len(seg_list) < 7:
            print('不够7个segment')
            continue

        # 合并segments; 返回一个job对象
        job = segments.merge(force=True)

        # 查看job进度
        job.refresh(inplace=True).progress


def merge_last_week(cube, ymd):
    """合并某天的上个星期的segments

    :param cube:
    :param ymd: 日期，比如 20200501
    :return:
    """
    ymd = datetime.strptime(ymd, '%Y%m%d')
    print(ymd)

    # 构造自然周的start 日期， 星期一
    start = ymd + timedelta(days=-ymd.weekday(), weeks=-1)

    # 构造自然周的start 日期， 星期日
    end = start + timedelta(days=7)

    # 处理时区问题
    start = start + timedelta(hours=8)
    end = end + timedelta(hours=8)

    # start 要加一分钟 过滤出上个月的segment。（KE API问题）
    start = start + timedelta(minutes=1)

    print(start)
    print(end)
    # 获取segments对象
    segments = cube.segments(start_time=start, end_time=end, size=1000)

    # 检查下segments的个数
    seg_list = segments.list_segments()
    print('segment numbers %s' % len(seg_list))

    if len(seg_list) <= 1:
        print('Note! segment number should be more than 1')
        return

    # 合并segments; 返回一个job对象
    job = segments.merge(force=True)

    # 查看job进度
    job.refresh(inplace=True).progress
    return job


def check_current_job_num():
    """
    获取当前在跑的任务数
    :return:
    """
    jobs = client.jobs(status=2)
    return len(jobs)


def check_segment_range(segments, year, month):
    """
    核查是否存在夸月的segment，以及segment个数等问题.
    :return: 返回None 或 将要合并的Segments
    """
    seg_list = segments.list_segments()

    # 过滤超出范围的segment
    seg_list = [seg for seg in seg_list if seg.date_range_start_dt >= datetime(year, month, 1)]
    next_month = datetime(year, month, 1) + relativedelta(months=+1)
    seg_list = [seg for seg in seg_list if seg.date_range_start_dt < next_month]
    print(seg_list)
    if len(seg_list) <= 1:
        print('segment个数小于等于一个不做处理')
        return
    seg_list = sorted(seg_list, key=lambda x: x.date_range_start)
    first_seg = seg_list[0]
    last_seg = seg_list[-1]
    # 最后一个segment的end日期 - start日期的相差天数
    last_seg_gap_days = (last_seg.date_range_end_dt - last_seg.date_range_start_dt).days

    if first_seg.date_range_start_dt.month == last_seg.date_range_end_dt.month:
        # 没有夸月
        return segments
    elif last_seg_gap_days > 20:
        if len(seg_list) >= 3:
            print('出现夸月情况，并且segment个数大于等于3时候，将最后一个segment剔除')
            seg_list = seg_list[-1]
            new_segments = Segments.from_segment_list(cube_name=segments.cube_name, client=client, segment_list=seg_list)
            return new_segments
        else:
            return
    else:
        new_segments = Segments.from_segment_list(cube_name=segments.cube_name, client=client, segment_list=seg_list)
        return new_segments


def merge_month(cube, year, month):
    """合并某个月的segments

    :param cube: Cube object
    :param year:  2020
    :param month: 3
    :return:
    """

    # 构造某个月的start 日期
    start = datetime(year, month, 1, 0, 0)

    # 构造 end
    end = start + relativedelta(months=+1)

    # 处理时区问题
    start = start + timedelta(hours=8)
    end = end + timedelta(hours=8)

    print(start)
    print(end)
    # 获取segments对象
    segments = cube.segments(start_time=start, end_time=end, size=1000)

    # 判断segments是否夸月等情况
    res = check_segment_range(segments, year, month)
    if res is None:
        return
    segments = res

    # 合并segments; 返回一个job对象
    job = segments.merge(force=True)

    # 查看job进度
    job.refresh(inplace=True).progress
    return job


if __name__ == '__main__':
    """
    运行方式：python example_merge_segment_3x.py 2019 1 kylin_sales_cube
    """
    year = int(sys.argv[1])
    month = int(sys.argv[2])  # 1月传参1
    cube_list = sys.argv[3]  # 逗号分隔每个cube
    cube_list = [c.strip() for c in cube_list.split(',')]

    for cube in cube_list:
        try:
            cube = client.cubes(cube)[0]
        except:
            print('Cube 获取失败')
            print(traceback.print_exc())
            continue
        while True:
            # 判断当前在跑的job数量有多少个，如果小于某个数，则执行后续合并；否则一直等待。
            job_num = check_current_job_num()
            print('当前正在running的job个数: %s' % job_num)
            if job_num < 3:
                break
            time.sleep(60)
        merge_month(cube, year, month)

