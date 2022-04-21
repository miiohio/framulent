from framulent.engine import Engine

"""
Let's try something:

1. Add 10 to all of the dimensions.
2. Calculate the product of petal length and width
3. Group by variety
4. Calculate the averages of all of the results

Obviously the "join by ROWID" stuff below is a bad idea (in general), but we'll
do it anyway just to exercise the approach.
"""

engine = Engine()

iris = engine.read_csv(
    table_name="iris",
    column_def="""
        "sepal.length" DOUBLE,
        "sepal.width" DOUBLE,
        "petal.length" DOUBLE,
        "petal.width" DOUBLE,
        variety VARCHAR
    """,
    csv="iris.csv"
)
# reveal_type(iris)

df1 = engine.query(
    f"""
    SELECT
        \"sepal.length\" + 10 as q
        ,rowid AS r
    FROM
        {iris}
    """
)
# reveal_type(df1)

df2 = engine.query(
    f"""
    SELECT
        \"sepal.width\" + 10 as q
        ,rowid AS r
    FROM
        {iris}
    """
)
# reveal_type(df2)

df3 = engine.query(
    f"""
    SELECT
        \"petal.length\" + 10 as q
        ,rowid AS r
    FROM
        {iris}
    """
)
# reveal_type(df3)

df4 = engine.query(
    f"""
    SELECT
        \"petal.width\" + 10 as q
        ,rowid AS r
    FROM
        {iris}
    """
)
# reveal_type(df4)

# 2. Calculate the product of petal length and width
prod = engine.query(
    f"""
    SELECT
        \"petal.width\" * \"petal.length\" as q
        ,rowid AS r
    FROM
        {iris}
    """
)
# reveal_type(prod)

rejoined = engine.query(
    f"""
    SELECT
        t1.q AS alpha,
        {df2}.q AS bravo,
        t3.q AS charlie,
        t4.q AS delta,
        t5.q AS echo,
        t1.r AS r
    FROM
        {df1} t1
        INNER JOIN {df2}
            ON t1.r = {df2}.r
        INNER JOIN {df3} t3
            ON t1.r = t3.r
        INNER JOIN {df4} t4
            ON t1.r = t4.r
        INNER JOIN {prod} t5
            ON t1.r = t5.r
    """
)
# reveal_type(rejoined)

# 3. Group by variety
# 4. Calculate the averages of all of the results
grouped = engine.query(
    f"""
    SELECT
        t2.variety,
        avg(t1.alpha),
        avg(t1.bravo),
        avg(t1.charlie),
        avg(t1.delta),
        avg(t1.echo)
    FROM
        {rejoined} t1
        INNER JOIN {iris} t2
            ON t1.r = t2.rowid
    GROUP BY
        t2.variety
    """,
    t1=rejoined,
    t2=iris
)
# reveal_type(grouped)

for elem in grouped.fetchall():
    print(elem)

print(grouped.schema)
