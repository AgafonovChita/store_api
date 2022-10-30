"""
row sql-query для выгрузки данных о пользователях и принадлежащих им кошельках в формате
[ {"id":555, "login": admin,
            "wallets": [{"id":5551, "balance": 4000}, {"id": 5552, "balance": 143}]},
  {"id":666, "login": admin1,
            "wallets": [{"id":6661, "balance": 3800}, {"id": 6662, "balance": 143}]},
"""
users_and_wallets_sql = """select row_to_json(user_and_wallets)
                        from (
                          select id as user_id, login,
                            (
                              select array_to_json(array_agg(row_to_json(wallets_list)))
                              from (
                                select id as wallet_id, balance as wallet_balance
                                from wallets
                                where owner_id=users.id
                              ) wallets_list
                            ) as wallets
                          from users
                        ) user_and_wallets;"""


"""row sql-query для периодического удаления из БД 'протухших' refresh-token"""
delete_expired_tokens = """delete from refresh_tokens
                        where exp < EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'))"""
