import click as c
import pandas as pd
import pytz
from datetime import datetime
from .connection.connect import *
from .models.config import *
from .models.position import *
from .models.financial import *


@c.group()
@c.option('--db-user', envvar='DB_CLI_USER', required=True)
@c.option('--db-pwd', envvar='DB_CLI_PWD', required=True)
@c.option('--db-host', default='127.0.0.1:27017', required=True)
@c.pass_context
def cydb(ctx, db_user, db_pwd, db_host):
    ctx.ensure_object(dict)
    ctx.obj['db_u'] = db_user
    ctx.obj['db_p'] = db_pwd
    ctx.obj['db_h'] = db_host


@cydb.command()
@c.option('--key', type=str, prompt=True, required=True)
@c.option('--secret', type=str, prompt=True, required=True)
@c.password_option(confirmation_prompt=False, required=False)
@c.option('--type',
          type=c.Choice(['okex', 'hbp', 'binance'], case_sensitive=False), prompt=True)
@c.pass_context
def add_ccxt_config(ctx, key, secret, password, type):
    # 添加 ccxt 配置
    # connect db
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_CONFIG)
    # save config
    e_type = 0
    if type == 'hbp':
        e_type = CCXTExchangeType.HuobiPro
    elif type == 'okex':
        e_type = CCXTExchangeType.Okex
    elif type == 'binance':
        e_type = CCXTExchangeType.Binance
    result = CCXTConfiguration(identifier=Sequence.fetch_next_id(CN_CCXT_CONFIG),
                               app_key=key,
                               app_secret=secret,
                               app_pw=password,
                               e_type=e_type).save()
    c.echo('Result: {}(id: {})'.format(result, result.identifier))


@cydb.command()
@c.pass_context
def aims_profit(ctx):
    # AMIS 收益
    pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
    # connect db
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_POSITION)
    connect_db_env(db_name=DB_POSITION)
    selling = list(AIMSPositionSelling.objects.values())
    df = pd.DataFrame(selling)
    df.drop(['_cls', '_id'], axis=1, inplace=True)
    print("""
    {}
    sum: {}
    """.format(df, df['profit_amount'].sum()))


@cydb.command()
@c.pass_context
def aims_position(ctx):
    # AMIS 仓位
    pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
    # connect db
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_POSITION)
    connect_db_env(db_name=DB_POSITION)
    selling = list(AIMSPosition.objects.aggregate({
        '$addFields': {
            'average_costing':
            {
                '$cond': {
                    'if': {'$gt': ['$hold', 0]},
                    'then': {'$divide': ['$cost', '$hold']},
                    'else': 0
                }
            }
        }
    }))
    df = pd.DataFrame(selling)
    df.drop(['_cls', '_id'], axis=1, inplace=True)
    print(df)


@cydb.command()
@c.option('--exchange', type=str, prompt=True, required=True)
@c.option('--coin_pair', type=str, prompt=True, required=True)
@c.option('--cost', type=float, prompt=True, required=True)
@c.option('--amount', type=float, prompt=True, required=True)
@c.pass_context
def add_aip_record(ctx, exchange, coin_pair, cost, amount):
    """添加定投记录"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_POSITION)
    record = AIPRecord()
    record.exchange = exchange
    record.coin_pair = coin_pair.upper()
    record.cost = cost
    record.amount = amount
    record.date = datetime.now()
    record.save()


@c.group()
@c.option('--db-user', envvar='DB_CLI_USER', required=True)
@c.option('--db-pwd', envvar='DB_CLI_PWD', required=True)
@c.option('--db-host', default='127.0.0.1:27017', required=True)
@c.pass_context
def cyfin(ctx, db_user, db_pwd, db_host):
    ctx.ensure_object(dict)
    ctx.obj['db_u'] = db_user
    ctx.obj['db_p'] = db_pwd
    ctx.obj['db_h'] = db_host
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_FINANCIAL)
    print("Current holders:")
    for holder in list(Holder.objects.project({'id': 1, "name": 1, 'balance': 1, 'update_date': 1}).values()):
        print("{}:\t{}\t{}\t{}".format(holder['_id'], holder['name'], holder['balance'], holder['update_date']))
    print()


@cyfin.command()
@c.option('--name', type=str, prompt=True, required=True)
@c.option('--balance', type=float, prompt=True, default=0, required=True)
@c.option('--level',
          type=c.Choice(['SUPER', 'A'], case_sensitive=False), default='A', prompt=True)
@c.pass_context
def add_holder(ctx, name, balance, level):
    """添加持仓人"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_FINANCIAL)
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_CONFIG)
    if len(list(Holder.objects.raw({'name': {"$regex": name, "$options": '-i'}}))) > 0:
        print('{}已存在'.format(name.upper()))
        return
    holder = Holder()
    holder.id = Sequence.fetch_next_id(CN_FIN_HOLDER)
    holder.name = name
    holder.balance = balance
    holder.level = HolderLevel.level_from(level).value
    holder.create_date = datetime.now().astimezone(tz=pytz.utc)
    holder.update_date = holder.create_date
    holder.save()


@cyfin.command()
@c.option('--holder_id', type=int, prompt=True, required=True)
@c.option('--operation', type=c.Choice(['deposit', 'withdraw'], case_sensitive=False), prompt=True, default='deposit', required=True)
@c.option('--amount', type=float, prompt='Amount[USDT]')
@c.pass_context
def update_holder_balance(ctx, holder_id, operation, amount):
    """更新持仓人余额"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_FINANCIAL)
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_CONFIG)
    try:
        holder = Holder.objects.get({'_id': holder_id})
        # event
        event = Event(id=Sequence.fetch_next_id(CN_FIN_EVENT), content=operation,
                      note=str(amount), date=holder.update_date)
        event.save()
        # record
        record = Record(holder=holder_id, event=event.id, date=holder.update_date)

        record.balance_before = holder.balance
        if operation.lower() == 'deposit':
            holder.balance += amount
        else:
            holder.balance -= amount
        record.balance_after = holder.balance

        holder.update_date = datetime.now().replace(tzinfo=pytz.utc)
        holder.save()
        record.save()
        holder.print_desc()
    except Exception as e:
        print(str(e))
        return


@cyfin.command()
@c.option('--holder_id', type=int, prompt=True, required=True)
@c.pass_context
def holder_events(ctx, holder_id):
    """持仓人事件记录"""
    connect_db(ctx.obj['db_u'], ctx.obj['db_p'], ctx.obj['db_h'], DB_FINANCIAL)
    pipeline = [
        {
            '$lookup': {
                'from': 'op_record',
                'localField': '_id',
                'foreignField': 'holder',
                'as': 'record'
            }
        }, {
            '$unwind': {
                'path': '$record',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$lookup': {
                'from': 'event',
                'localField': 'record.event',
                'foreignField': '_id',
                'as': 'event'
            }
        }, {
            '$unwind': {
                'path': '$event',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$addFields': {
                'event_content': '$event.content',
                'event_note': '$event.note',
                'event_date': '$event.date',
                'balance_before': '$record.balance_before',
                'balance_after': '$record.balance_after',
            }
        }, {
            '$project': {
                '_id': 1,
                'name': 1,
                'balance': 1,
                'event_content': 1,
                'event_note': 1,
                'event_date': 1,
                'balance_before': 1,
                'balance_after': 1
            }
        }
    ]
    records = list(Holder.objects.raw({'_id': holder_id}).aggregate(*pipeline))
    for record in records:
        print("{}: \t{}\t{}\t{}\t{}\t{}\t{}".format(
            holder_id, record['name'], record['balance_before'], record['balance_after'], record['event_content'], record['event_note'], record['event_date']))
