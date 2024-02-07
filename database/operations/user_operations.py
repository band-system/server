from database.schema.models import *
import sqlalchemy as sa

def model_to_dict(object):
    return {c.name: getattr(object, c.name) for c in object.__table__.columns}

def userExist(id: str):
    exist = db.select(
        User
    ).where(
        User.id == id
    )
    result = db.session.scalars(exist).all()
    return len(result) != 0

def get_user_password(user_id):
    password = db.select(
        User.password
    ).where(
        User.id == user_id
    )
    return db.session.scalar(password)

def get_user_by_id(user_id):
    if not userExist(user_id):
        return 404

    basic_info_q = db.select(
        User
    ).where(
        User.id == user_id
    )
    basic_info = db.session.scalar(basic_info_q)
    # basic_info = model_to_dict(basic_info)
    instrument_q = db.select(
        User_Instrument.c.instrument_id
    ).where(
        User_Instrument.c.user_id == user_id
    )

    instrument = db.session.scalars(instrument_q).all()

    region_q = db.select(
        User_Region.c.region_id
    ).where(
        User_Region.c.user_id == user_id
    )

    region = db.session.scalars(region_q).all()

    style_q = db.select(
        User_Style.c.style_id
    ).where(
        User_Style.c.user_id == user_id
    )

    style = db.session.scalars(style_q).all()

    return basic_info, instrument, region, style


def get_instrument_by_user(user_id):
    query = db.select(
        User_Instrument.c.instrument_id
    ).where(
        User_Instrument.c.user_id == user_id
    )

    return db.session.scalars(query).all()

def get_region_by_user(user_id):
    query = db.select(
        User_Region.c.region_id
    ).where(
        User_Region.c.user_id == user_id
    )

    return db.session.scalars(query).all()

def get_style_by_user(user_id):
    query = db.select(
        User_Style.c.style_id
    ).where(
        User_Style.c.user_id == user_id
    )

    return db.session.scalars(query).all()

def queryUserByString(search):
    query = db.select(
        User.id,
        User.name,
        User.photo
    ).where(
        User.name.contains(search)
    )
    return db.session.scalars(query).all()


def updateUserInstruments(user_id ,new_ids):
    if len(new_ids) == 0:
        return
    cur_ids = get_instrument_by_user(user_id)
    
    for i in cur_ids:
        if i not in new_ids:
            del_stmt = db.delete(
                User_Instrument
            ).where(
                User_Instrument.c.user_id == user_id
            ).where(
                User_Instrument.c.instrument_id == i
            )
            db.session.execute(del_stmt)

    for i in new_ids:
        if i not in cur_ids:
            ins_stmt = db.insert(
                User_Instrument
            ).values(
                user_id = user_id,
                instrument_id = i
            )
            db.session.execute(ins_stmt)
    db.session.commit()
    return

    

def updateUserRegions(user_id ,new_ids):
    if len(new_ids) == 0:
        return
    cur_ids = get_region_by_user(user_id)

    for i in cur_ids:
        if i not in new_ids:
            del_stmt = db.delete(
                User_Region
            ).where(
                User_Region.c.user_id == user_id
            ).where(
                User_Region.c.region_id == i
            )
            db.session.execute(del_stmt)

    for i in new_ids:
        if i not in cur_ids:
            ins_stmt = db.insert(
                User_Region
            ).values(
                user_id = user_id,
                region_id = i
            )
            db.session.execute(ins_stmt)
    db.session.commit()
    return



def updateUserStyles(user_id ,new_ids):
    if len(new_ids) == 0:
        return
    cur_ids = get_style_by_user(user_id)

    for i in cur_ids:
        if i not in new_ids:
            del_stmt = db.delete(
                User_Style
            ).where(
                User_Style.c.user_id == user_id
            ).where(
                User_Style.c.style_id == i
            )
            db.session.execute(del_stmt)

    for i in new_ids:
        if i not in cur_ids:
            ins_stmt = db.insert(
                User_Style
            ).values(
                user_id = user_id,
                style_id = i
            )
            db.session.execute(ins_stmt)
    db.session.commit()
    return


def updateUser(user_id, name, bio, prefered_time, email, ig, fb, photo):
    if photo == "not Exist":
        stmt = db.update(
            User
        ).where(
            User.id == user_id
        ).values(
            name = name,
            bio = bio,
            prefered_time = prefered_time,
            email = email,
            ig = ig,
            fb = fb
        )
        db.session.execute(stmt)
        db.session.commit()
        return

    stmt = db.update(
        User
    ).where(
        User.id == user_id
    ).values(
        name = name,
        bio = bio,
        prefered_time = prefered_time,
        email = email,
        ig = ig,
        fb = fb,
        photo = photo
    )
    
    db.session.execute(stmt)
    db.session.commit()
    return

def sendBandJoinRequest(user_id, band_id):
    
    stmt = db.insert(
        User_Band
    ).values(
        user_id = user_id,
        band_id = band_id,
        status = 0 
    )
    db.session.execute(stmt)
    db.session.commit()
    return

def updateUserPassword(user_id, password):
    stmt = db.update(
        User
    ).where(
        User.id == user_id
    ).values(
        password = password
    )
    
    db.session.execute(stmt)
    db.session.commit()
    return


def queryCompatibleMusician(instruments, regions, styles):

    instruments = [int(i) for i in instruments]
    regions = [str(i) for i in regions]
    styles = [int(i) for i in styles]

    instrument_count = db.select(
        User_Instrument.c.user_id,
        db.func.count(User_Instrument.c.instrument_id).label('count')
    ).where(
        User_Instrument.c.instrument_id.in_(instruments)
    ).group_by(
        User_Instrument.c.user_id
    ).cte()

    region_count = db.select(
        User_Region.c.user_id,
        db.func.count(User_Region.c.region_id).label('count')
    ).where(
        User_Region.c.region_id.in_(regions)
    ).group_by(
        User_Region.c.user_id
    ).cte()

    style_count = db.select(
        User_Style.c.user_id,
        db.func.count(User_Style.c.style_id).label('count')
    ).where(
        User_Style.c.style_id.in_(styles)
    ).group_by(
        User_Style.c.user_id
    ).cte()

    subq = db.select(
        User.id.label('user_id'),
        User.name.label('name'),
        User.photo.label('photo'),
        db.func.coalesce(instrument_count.c.count, 0).label('instrument_count'),
        db.func.coalesce(region_count.c.count, 0).label('region_count'),
        db.func.coalesce(style_count.c.count, 0).label('style_count'),
        
    ).join(
        instrument_count,
        User.id == instrument_count.c.user_id,
        full = True
    ).join(
        region_count,
        User.id == region_count.c.user_id,
        full = True
    ).join(
        style_count,
        User.id == style_count.c.user_id,
        full = True
    ).where(
       (db.func.coalesce(instrument_count.c.count, 0)+ db.func.coalesce(region_count.c.count, 0) + db.func.coalesce(style_count.c.count, 0)) > 0
    )

    
    result = db.session.execute(subq).all()
    return [row._asdict() for row in result]



    
                            



