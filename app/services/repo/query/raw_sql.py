users_and_wallets_sql = """select row_to_json(user_and_wallets)
                        from (
                          select id, login,
                            (
                              select array_to_json(array_agg(row_to_json(wallets_list)))
                              from (
                                select id, balance
                                from wallets
                                where owner_id=users.id
                              ) wallets_list
                            ) as wallets
                          from users
                        ) user_and_wallets;"""



delete_expired_tokens = """delete from refresh_tokens
                        where exp > EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'))"""

