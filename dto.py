from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import UniqueConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import DATETIME
from sqlalchemy import DECIMAL
from sqlalchemy import INTEGER
from sqlalchemy import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from app.utils import get_now
from app.infrastructures.mysql_repositories.mysql_driver import Base
from app.domains.models.ability import Ability
from app.domains.models.charactor import Charactor
from app.domains.models.item import Item
from app.domains.models.move import Move
from app.domains.models.my_party import MyParty
from app.domains.models.my_pokemon import MyPokemon
from app.domains.models.pokemon import Pokemon


class AbilityDto(Base):
    __tablename__ = 'abilities'
    ability_name: str = Column(VARCHAR(20), primary_key=True)
    ability_detail: str = Column(VARCHAR(1000))

    def to_entity(self) -> Ability:
        return Ability(ability_name=self.ability_name, ability_detail=self.ability_detail)


class MoveDto(Base):
    __tablename__ = 'moves'
    move_id: int = Column(INTEGER, primary_key=True, autoincrement=True)
    move_name: str = Column(VARCHAR(30), nullable=False)
    move_class: str = Column(VARCHAR(10), nullable=False)
    move_type: str = Column(VARCHAR(10), nullable=False)
    damage: int = Column(INTEGER)
    hit_rate: int = Column(INTEGER)
    pp: int = Column(INTEGER, nullable=False)
    move_detail: str = Column(VARCHAR(1000))

    pokemons = relationship('PokemonDto', secondary='move_sets', back_populates='moves')

    def to_entity(self) -> Move:
        return Move(
            move_id=self.move_id,
            move_name=self.move_name,
            move_type=self.move_type,
            move_class=self.move_class,
            damage=self.damage,
            hit_rate=self.hit_rate,
            pp=self.pp,
            move_detail=self.move_detail
        )


class PokemonDto(Base):
    __tablename__ = 'pokemons'
    pokemon_id: int = Column(INTEGER, primary_key=True, autoincrement=True)
    pokemon_name: str = Column(VARCHAR(20), nullable=False)
    kind: str = Column(VARCHAR(20))
    type_1: str = Column(VARCHAR(10), nullable=False)
    type_2: str = Column(VARCHAR(10))
    h: int = Column(INTEGER, nullable=False)
    a: int = Column(INTEGER, nullable=False)
    b: int = Column(INTEGER, nullable=False)
    c: int = Column(INTEGER, nullable=False)
    d: int = Column(INTEGER, nullable=False)
    s: int = Column(INTEGER, nullable=False)
    ability_name_1: str = Column(VARCHAR(20), ForeignKey('abilities.ability_name'), nullable=False)
    ability_name_2: str = Column(VARCHAR(20), ForeignKey('abilities.ability_name'))
    ability_name_3: str = Column(VARCHAR(20), ForeignKey('abilities.ability_name'))

    ability_1: Mapped[AbilityDto] = relationship('AbilityDto', foreign_keys=[ability_name_1])
    ability_2: Mapped[AbilityDto] = relationship('AbilityDto', foreign_keys=[ability_name_2])
    ability_3: Mapped[AbilityDto] = relationship('AbilityDto', foreign_keys=[ability_name_3])
    moves: Mapped[List[MoveDto]] = relationship('MoveDto', secondary='move_sets', back_populates='pokemons')

    def to_entity(self) -> Pokemon:
                
        types = [self.type_1]
        if self.type_2 is not None:
            types.append(self.type_2)

        abilities = [Ability(self.ability_1.ability_name, self.ability_1.ability_detail)]

        if self.ability_2 is not None:
            abilities.append(Ability(self.ability_2.ability_name, self.ability_2.ability_detail))

        if self.ability_3 is not None:
            abilities.append(Ability(self.ability_3.ability_name, self.ability_3.ability_detail))

        moves: List[Move] = []
        for move_dto in self.moves:
            moves.append(Move(
                move_id=move_dto.move_id,
                move_name=move_dto.move_name,
                move_type=move_dto.move_type,
                move_class=move_dto.move_class,
                damage=move_dto.damage,
                hit_rate=move_dto.hit_rate,
                pp=move_dto.pp,
                move_detail=move_dto.move_detail))


        pokemon: Pokemon = Pokemon(
            pokemon_id=self.pokemon_id,
            pokemon_name=self.pokemon_name,
            kind=self.kind,
            types=types,
            abilities=abilities,
            moves=moves,
            h=self.h,
            a=self.a,
            b=self.b,
            c=self.c,
            d=self.d,
            s=self.s
        )

        return pokemon


class MoveSetDto(Base):
    __tablename__ = 'move_sets'
    __table_args__ = (UniqueConstraint('pokemon_id', 'move_id'), {})
    move_set_id: int = Column(INTEGER, primary_key=True, autoincrement=True)
    pokemon_id: int = Column(INTEGER, ForeignKey('pokemons.pokemon_id'), nullable=False)
    move_id: int = Column(INTEGER, ForeignKey('moves.move_id'), nullable=False)


class ItemDto(Base):
    __tablename__ = 'items'
    item_name: str = Column(VARCHAR(20), primary_key=True)
    item_detail: str = Column(VARCHAR(1000))

    def to_entity(self) -> Item:
        return Item(item_name=self.item_name, item_detail=self.item_detail)



class CharactorDto(Base):
    __tablename__ = 'charactors'
    charactor_name: str = Column(VARCHAR(10), primary_key=True)
    a_correction: float = Column(DECIMAL(2, 1), nullable=False)
    b_correction: float = Column(DECIMAL(2, 1), nullable=False)
    c_correction: float = Column(DECIMAL(2, 1), nullable=False)
    d_correction: float = Column(DECIMAL(2, 1), nullable=False)
    s_correction: float = Column(DECIMAL(2, 1), nullable=False)

    def to_entity(self) -> Charactor:
        return Charactor(charactor_name=self.charactor_name,
                         a_correction=self.a_correction,
                         b_correction=self.b_correction,
                         c_correction=self.c_correction,
                         d_correction=self.d_correction,
                         s_correction=self.s_correction)


class MyPokemonDto(Base):
    __tablename__ = 'my_pokemons'
    __table_args__ = (UniqueConstraint('pokemon_id', 'pokemon_nn'), {})
    my_pokemon_id: int = Column(INTEGER, primary_key=True, autoincrement=True)
    pokemon_id: int = Column(INTEGER, ForeignKey('pokemons.pokemon_id'), nullable=False)
    pokemon_nn: str = Column(VARCHAR(20))
    my_pokemon_detail: str = Column(VARCHAR(1000))
    item_name: str = Column(VARCHAR(20), ForeignKey('items.item_name'))
    ability_name: str = Column(VARCHAR(20), ForeignKey('abilities.ability_name'), nullable=False)
    charactor_name: str = Column(VARCHAR(10), ForeignKey('charactors.charactor_name'), nullable=False)
    effort_h: int = Column(INTEGER, nullable=False)
    effort_a: int = Column(INTEGER, nullable=False)
    effort_b: int = Column(INTEGER, nullable=False)
    effort_c: int = Column(INTEGER, nullable=False)
    effort_d: int = Column(INTEGER, nullable=False)
    effort_s: int = Column(INTEGER, nullable=False)
    move_id_1: int = Column(INTEGER, ForeignKey('moves.move_id'), nullable=False)
    move_id_2: int = Column(INTEGER, ForeignKey('moves.move_id'))
    move_id_3: int = Column(INTEGER, ForeignKey('moves.move_id'))
    move_id_4: int = Column(INTEGER, ForeignKey('moves.move_id'))
    terastal_type: str = Column(VARCHAR(10), nullable=False)
    create_at: datetime = Column(DATETIME, default=get_now())
    updated_at: datetime = Column(DATETIME, default=get_now(), onupdate=get_now())

    pokemon: Mapped[PokemonDto] = relationship('PokemonDto', foreign_keys=[pokemon_id])
    ability: Mapped[AbilityDto] = relationship('AbilityDto', foreign_keys=[ability_name])
    item: Mapped[ItemDto] = relationship('ItemDto', foreign_keys=[item_name])
    charactor: Mapped[CharactorDto] = relationship('CharactorDto', foreign_keys=[charactor_name])
    move_1: Mapped[MoveDto] = relationship('MoveDto', foreign_keys=[move_id_1])
    move_2: Mapped[MoveDto] = relationship('MoveDto', foreign_keys=[move_id_2])
    move_3: Mapped[MoveDto] = relationship('MoveDto', foreign_keys=[move_id_3])
    move_4: Mapped[MoveDto] = relationship('MoveDto', foreign_keys=[move_id_4])

    @classmethod
    def from_entity(cls, my_pokemon: MyPokemon) -> 'MyPokemonDto':

        item_name = None
        if my_pokemon.item is not None:
            item_name = my_pokemon.item.item_name

        move_ids = [None, None, None, None]

        for idx in range(len(my_pokemon.moves)):
            move_ids[idx] = my_pokemon.moves[idx].move_id

        dto: MyPokemonDto = MyPokemonDto(
            my_pokemon_id=my_pokemon.my_pokemon_id,
            pokemon_id=my_pokemon.pokemon.pokemon_id,
            pokemon_nn=my_pokemon.my_pokemon_name,
            my_pokemon_detail=my_pokemon.my_pokemon_detail,
            item_name=item_name,
            ability_name=my_pokemon.ability.ability_name,
            charactor_name=my_pokemon.charactor.charactor_name,
            effort_h=my_pokemon.effort_value_h,
            effort_a=my_pokemon.effort_value_a,
            effort_b=my_pokemon.effort_value_b,
            effort_c=my_pokemon.effort_value_c,
            effort_d=my_pokemon.effort_value_d,
            effort_s=my_pokemon.effort_value_s,
            move_id_1=move_ids[0],
            move_id_2=move_ids[1],
            move_id_3=move_ids[2],
            move_id_4=move_ids[3],
            terastal_type=my_pokemon.terastal_type
        )

        return dto
    
    def to_entity(self) -> MyPokemon:
        my_pokemon: MyPokemon = MyPokemon(
            pokemon=self.pokemon.to_entity(),
            my_pokemon_name=self.pokemon_nn,
            my_pokemon_detail=self.my_pokemon_detail,
            my_pokemon_id=self.my_pokemon_id,
            create_at=self.create_at,
            update_at=self.updated_at
        )

        if self.item is not None:
            my_pokemon.set_item(self.item.to_entity())

        if self.move_id_1 is not None:
            my_pokemon.set_move(self.move_1.to_entity())
        if self.move_id_2 is not None:
            my_pokemon.set_move(self.move_2.to_entity())
        if self.move_id_3 is not None:
            my_pokemon.set_move(self.move_3.to_entity())
        if self.move_id_4 is not None:
            my_pokemon.set_move(self.move_4.to_entity())

        my_pokemon.set_ability(self.ability.to_entity())
        my_pokemon.set_charactor(self.charactor.to_entity())
        my_pokemon.set_effort_values(self.effort_h, self.effort_a, self.effort_b, self.effort_c, self.effort_d, self.effort_s)
        my_pokemon.set_terastal_type(self.terastal_type)

        return my_pokemon


class MyPartyDto(Base):
    __tablename__ = 'my_parties'
    my_party_id: int = Column(INTEGER, primary_key=True)
    party_name: str = Column(VARCHAR(30), nullable=False, unique=True)
    party_detail: str = Column(VARCHAR(1000))
    my_pokemon_id_1: int = Column(INTEGER, ForeignKey('my_pokemons.my_pokemon_id'))
    my_pokemon_id_2: int = Column(INTEGER, ForeignKey('my_pokemons.my_pokemon_id'))
    my_pokemon_id_3: int = Column(INTEGER, ForeignKey('my_pokemons.my_pokemon_id'))
    my_pokemon_id_4: int = Column(INTEGER, ForeignKey('my_pokemons.my_pokemon_id'))
    my_pokemon_id_5: int = Column(INTEGER, ForeignKey('my_pokemons.my_pokemon_id'))
    my_pokemon_id_6: int = Column(INTEGER, ForeignKey('my_pokemons.my_pokemon_id'))
    create_at: datetime = Column(DATETIME, default=get_now())
    updated_at: datetime = Column(DATETIME, default=get_now(), onupdate=get_now())

    my_pokemon_1: Mapped[Optional[MyPokemonDto]] = relationship('MyPokemonDto', foreign_keys=[my_pokemon_id_1])
    my_pokemon_2: Mapped[Optional[MyPokemonDto]] = relationship('MyPokemonDto', foreign_keys=[my_pokemon_id_2])
    my_pokemon_3: Mapped[Optional[MyPokemonDto]] = relationship('MyPokemonDto', foreign_keys=[my_pokemon_id_3])
    my_pokemon_4: Mapped[Optional[MyPokemonDto]] = relationship('MyPokemonDto', foreign_keys=[my_pokemon_id_4])
    my_pokemon_5: Mapped[Optional[MyPokemonDto]] = relationship('MyPokemonDto', foreign_keys=[my_pokemon_id_5])
    my_pokemon_6: Mapped[Optional[MyPokemonDto]] = relationship('MyPokemonDto', foreign_keys=[my_pokemon_id_6])

    @classmethod
    def from_entity(cls, my_party: MyParty) -> 'MyPartyDto':

        my_pokemons: List[Optional[int]] = [None, None, None, None, None, None]
        for idx in range(len(my_party.my_pokemons)):
            my_pokemons[idx] = my_party.my_pokemons[idx].my_pokemon_id

        return MyPartyDto(
            my_party_id=my_party.party_id,
            party_name=my_party.party_name,
            party_detail=my_party.party_detail,
            my_pokemon_id_1=my_pokemons[0],
            my_pokemon_id_2=my_pokemons[1],
            my_pokemon_id_3=my_pokemons[2],
            my_pokemon_id_4=my_pokemons[3],
            my_pokemon_id_5=my_pokemons[4],
            my_pokemon_id_6=my_pokemons[5]
            )
    
    def to_entity(self) -> MyParty:
        my_party = MyParty(
            party_name=self.party_name,
            party_detail=self.party_detail,
            party_id=self.my_party_id,
            create_at=self.create_at,
            update_at=self.updated_at
        )

        if self.my_pokemon_1 is not None:
            my_party.set_my_pokemon(self.my_pokemon_1.to_entity())

        if self.my_pokemon_2 is not None:
            my_party.set_my_pokemon(self.my_pokemon_2.to_entity())

        if self.my_pokemon_3 is not None:
            my_party.set_my_pokemon(self.my_pokemon_3.to_entity())

        if self.my_pokemon_4 is not None:
            my_party.set_my_pokemon(self.my_pokemon_4.to_entity())

        if self.my_pokemon_5 is not None:
            my_party.set_my_pokemon(self.my_pokemon_5.to_entity())

        if self.my_pokemon_6 is not None:
            my_party.set_my_pokemon(self.my_pokemon_6.to_entity())

        return my_party


class DamageScaleDto(Base):
    __tablename__ = 'damage_scales'
    damage_scale_id: int = Column(INTEGER, primary_key=True)
    attack_type: str = Column(VARCHAR(10), nullable=False)
    defence_type_1: str = Column(VARCHAR(10), nullable=False)
    defence_type_2: str = Column(VARCHAR(10), nullable=False)
