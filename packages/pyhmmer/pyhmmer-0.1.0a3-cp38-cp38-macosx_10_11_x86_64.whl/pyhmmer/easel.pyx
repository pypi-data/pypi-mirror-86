# coding: utf-8
# cython: language_level=3, linetrace=True
"""High-level interface to the Easel C library.

Easel is a library developed by the `Eddy/Rivas Lab <http://eddylab.org/>`_
to facilitate the development of biological software in C. It is used by
`HMMER <http://hmmer.org/>`_ and `Infernal <http://eddylab.org/infernal/>`_.

"""

# --- C imports --------------------------------------------------------------

cimport cython
from libc.stdint cimport uint32_t
from libc.stdlib cimport malloc
from libc.string cimport memmove, strdup, strlen
from cpython.unicode cimport PyUnicode_FromUnicode

cimport libeasel
cimport libeasel.alphabet
cimport libeasel.bitfield
cimport libeasel.keyhash
cimport libeasel.sq
cimport libeasel.sqio
from libeasel cimport ESL_DSQ

DEF eslERRBUFSIZE = 128

# --- Python imports ---------------------------------------------------------

import os
import warnings

from .errors import AllocationError, UnexpectedError


# --- Cython classes ---------------------------------------------------------

cdef class Alphabet:
    """A biological alphabet, including additional marker symbols.
    """

    # --- Default constructors -----------------------------------------------

    cdef _init_default(self, int ty):
        self._abc = libeasel.alphabet.esl_alphabet_Create(ty)
        if not self._abc:
            raise AllocationError("ESL_ALPHABET")

    @classmethod
    def amino(cls):
        """Create a default amino-acid alphabet.
        """
        cdef Alphabet alphabet = Alphabet.__new__(Alphabet)
        alphabet._init_default(libeasel.alphabet.eslAMINO)
        return alphabet

    @classmethod
    def dna(cls):
        """Create a default DNA alphabet.
        """
        cdef Alphabet alphabet = Alphabet.__new__(Alphabet)
        alphabet._init_default(libeasel.alphabet.eslDNA)
        return alphabet

    @classmethod
    def rna(cls):
        """Create a default RNA alphabet.
        """
        cdef Alphabet alphabet = Alphabet.__new__(Alphabet)
        alphabet._init_default(libeasel.alphabet.eslRNA)
        return alphabet

    # def __init__(self, str alphabet, int K, int Kp):
    #     buffer = alphabet.encode('ascii')
    #     self._alphabet = libeasel.alphabet.esl_alphabet_CreateCustom(<char*> buffer, K, Kp)
    #     if not self._alphabet:
    #         raise AllocationError("ESL_ALPHABET")

    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self._abc = NULL

    def __dealloc__(self):
        libeasel.alphabet.esl_alphabet_Destroy(self._abc)

    def __repr__(self):
        if self._abc.type == libeasel.alphabet.eslRNA:
            return "Alphabet.rna()"
        elif self._abc.type == libeasel.alphabet.eslDNA:
            return "Alphabet.dna()"
        elif self._abc.type == libeasel.alphabet.eslAMINO:
            return "Alphabet.amino()"
        else:
            return "Alphabet({!r}, K={!r}, Kp={!r})".format(
                self._abc.sym.decode('ascii'),
                self._abc.K,
                self._abc.Kp
            )

    def __eq__(self, Alphabet other):
        if other is None:
            return False
        return self._abc.type == other._abc.type   # FIXME

    def __getstate__(self):
        return {"type": self._abc.type}

    def __setstate__(self, state):
        self._init_default(state["type"])


    # --- Properties ---------------------------------------------------------

    @property
    def K(self):
        """`int`: The alphabet size, counting only actual alphabet symbols.

        Example:
            >>> Alphabet.dna().K
            4
            >>> Alphabet.amino().K
            20

        """
        return self._abc.K

    @property
    def Kp(self):
        """`int`: The complete alphabet size, including marker symbols.

        Example:
            >>> Alphabet.dna().Kp
            18
            >>> Alphabet.amino().Kp
            29

        """
        return self._abc.Kp

    @property
    def symbols(self):
        """`str`: The symbols composing the alphabet.

        Example:
            >>> Alphabet.dna().symbols
            'ACGT-RYMKSWHBVDN*~'
            >>> Alphabet.rna().symbols
            'ACGU-RYMKSWHBVDN*~'

        """
        cdef bytes symbols = self._abc.sym[:self._abc.Kp]
        return symbols.decode("ascii")


cdef class Bitfield:
    """A statically sized sequence of booleans stored as a packed bitfield.
    """

    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self._b = NULL

    def __dealloc__(self):
        libeasel.bitfield.esl_bitfield_Destroy(self._b)

    def __init__(self, size_t length):
        self._b = libeasel.bitfield.esl_bitfield_Create(length)
        if not self._b:
            raise AllocationError("ESL_BITFIELD")

    def __len__(self):
        assert self._b != NULL
        return self._b.nb

    def __getitem__(self, index):
        assert self._b != NULL
        cdef size_t index_ = self._wrap_index(index)
        return libeasel.bitfield.esl_bitfield_IsSet(self._b, index_)

    def __setitem__(self, index, value):
        assert self._b != NULL
        cdef size_t index_ = self._wrap_index(index)
        if value:
            libeasel.bitfield.esl_bitfield_Set(self._b, index_)
        else:
            libeasel.bitfield.esl_bitfield_Clear(self._b, index_)

    cdef size_t _wrap_index(self, int index):
        if index < 0:
            index += self._b.nb
        if index >= self._b.nb or index < 0:
            raise IndexError("bitfield index out of range")
        return <size_t> index

    cpdef size_t count(self, bint value=1):
        """Count the number occurrences of ``value`` in the bitfield.

        If no argument is given, counts the number of `True` occurences.

        Example:
            >>> bitfield = Bitfield(8)
            >>> bitfield.count(False)
            8
            >>> bitfield[0] = bitfield[1] = True
            >>> bitfield.count()
            2

        """
        assert self._b != NULL

        cdef size_t count_ = libeasel.bitfield.esl_bitfield_Count(self._b)
        return count_ if value else self._b.nb - count_

    cpdef void toggle(self, int index):
        """Switch the value of one single bit.

        Example:
            >>> bitfield = Bitfield(8)
            >>> bitfield[0]
            False
            >>> bitfield.toggle(0)
            >>> bitfield[0]
            True
            >>> bitfield.toggle(0)
            >>> bitfield[0]
            False

        """
        assert self._b != NULL
        cdef size_t index_ = self._wrap_index(index)
        libeasel.bitfield.esl_bitfield_Toggle(self._b, index_)


cdef class KeyHash:
    """A dynamically resized container to store string keys using a hash table.
    """

    def __cinit__(self):
        self._kh = NULL

    def __dealloc__(self):
        libeasel.keyhash.esl_keyhash_Destroy(self._kh)

    def __init__(self):
        self._kh = libeasel.keyhash.esl_keyhash_Create()
        if not self._kh:
            raise AllocationError("ESL_KEYHASH")

    def __copy__(self):
        return self.copy()

    def __len__(self):
        assert self._kh != NULL
        return libeasel.keyhash.esl_keyhash_GetNumber(self._kh)

    def __contains__(self, value):
        assert self._kh != NULL
        if isinstance(bytes, value):
            status = libeasel.keyhash.esl_keyhash_Lookup(self._kh, <const char*> value, len(value), NULL)
            if status == libeasel.eslOK:
                return True
            elif status == libeasel.eslENOTFOUND:
                return False
            else:
                raise UnexpectedError(status, "esl_keyhash_Lookup")
        else:
            ty = type(value).__name__
            raise TypeError("'in <KeyHash>' requires string as left operand, not {}".format(ty))

    cpdef void clear(self):
        cdef int status = libeasel.keyhash.esl_keyhash_Reuse(self._kh)
        if status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_keyhash_Reuse")

    cpdef KeyHash copy(self):
        assert self._kh != NULL
        cdef KeyHash new = KeyHash.__new__(KeyHash)
        new._kh = libeasel.keyhash.esl_keyhash_Clone(self._kh)
        if not new._kh:
            raise AllocationError("ESL_KEYHASH")
        return new


@cython.freelist(4)
cdef class Sequence:
    """An abstract biological sequence with some associated metadata.

    Easel provides two different mode to store a sequence: text, or digital.
    In the HMMER code, changing from one mode to another mode is done in
    place, which allows recycling memory. However, doing so can be confusing
    since there is no way to know statically the representation of a sequence.

    To avoid this, ``pyhmmer`` provides two subclasses of the `Sequence`
    abstract class to maintain the mode contract: `TextSequence` and
    `DigitalSequence`. Functions expecting sequences in digital format, like
    `pyhmmer.hmmsearch`, can then use Python type system to make sure they
    receive sequences in the right mode. This allows type checkers such as
    ``mypy`` to detect potential contract breaches at compile-time.

    """

    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self._sq = NULL

    def __init__(self):
        raise TypeError("Can't instantiate abstract class 'Sequence'")

    def __dealloc__(self):
        libeasel.sq.esl_sq_Destroy(self._sq)

    def __eq__(self, Sequence other):
        return libeasel.sq.esl_sq_Compare(self._sq, other._sq) == libeasel.eslOK

    # --- Properties ---------------------------------------------------------

    @property
    def accession(self):
        """`str` or `None`: The accession of the sequence, if any.
        """
        accession = <bytes> self._sq.acc
        return accession or None

    @accession.setter
    def accession(self, accession):
        if accession is None:
            accession = b""
        cdef int status = libeasel.sq.esl_sq_SetAccession(self._sq, <const char*> accession)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_SetAccession")

    @property
    def name(self):
        """`bytes`: The name of the sequence.
        """
        return <bytes> self._sq.name

    @name.setter
    def name(self, bytes name):
        cdef int status = libeasel.sq.esl_sq_SetName(self._sq, <const char*> name)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_SetName")

    @property
    def description(self):
        """`bytes`: The description of the sequence.
        """
        return <bytes> self._sq.desc

    @description.setter
    def description(self, desc):
        cdef int status = libeasel.sq.esl_sq_SetDesc(self._sq, <const char*> desc)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_SetDesc")

    @property
    def source(self):
        """`bytes`: The source of the sequence, if any.
        """
        return <bytes> self._sq.source

    @source.setter
    def source(self, src):
        if src is None:
            src = b""
        cdef int status = libeasel.sq.esl_sq_SetSource(self._sq, <const char*> src)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_SetSource")

    # --- Methods ------------------------------------------------------------

    cpdef uint32_t checksum(self):
        """Calculate a 32-bit checksum for the sequence.
        """
        cdef uint32_t checksum = 0
        cdef int status = libeasel.sq.esl_sq_Checksum(self._sq, &checksum)
        if status == libeasel.eslOK:
            return checksum
        else:
            raise UnexpectedError(status, "esl_sq_Checksum")

    cpdef void clear(self):
        """Reinitialize the sequence for re-use.
        """
        assert self._sq != NULL

        cdef int status = libeasel.sq.esl_sq_Reuse(self._sq)
        if status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_Reuse")


cdef class TextSequence(Sequence):
    """A biological sequence stored in text mode.
    """

    def __init__(
        self,
        bytes name=None,
        bytes description=None,
        bytes accession=None,
        bytes sequence=None,
        bytes secondary_structure=None
    ):
        self._sq = libeasel.sq.esl_sq_Create()
        if not self._sq:
            raise AllocationError("ESL_SQ")

        if name is not None:
            self.name = name
        if accession is not None:
            self.accession = accession
        if description is not None:
            self.description = description

    cpdef DigitalSequence digitize(self, Alphabet alphabet):
        """Convert the text sequence to a digital sequence using ``alphabet``.
        """
        cdef int status
        cdef DigitalSequence new

        new = DigitalSequence.__new__(DigitalSequence, alphabet)
        new._sq = libeasel.sq.esl_sq_CreateDigital(alphabet._abc)
        if new._sq == NULL:
            raise AllocationError("ESL_SQ")

        status = libeasel.sq.esl_sq_Copy(self._sq, new._sq)
        if status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_Copy")

        assert libeasel.sq.esl_sq_IsDigital(new._sq)
        return new


cdef class DigitalSequence(Sequence):
    """A biological sequence stored in digital mode.

    Currently, objects from this class cannot be instantiated directly. Use
    `TextSequence.digitize` to obtain a digital sequence from a sequence in
    text mode.

    Attributes:
        alphabet (`Alphabet`, *readonly*): The biological alphabet used to
            encode this sequence to digits.

    """

    def __cinit__(self, Alphabet alphabet):
        self.alphabet = alphabet


cdef class SequenceFile:
    """A wrapper around a sequence file, containing unaligned sequences.

    This class supports reading sequences stored in different formats, such
    as FASTA, GenBank or EMBL. The format of each file can be automatically
    detected, but it is also possible to pass an explicit format specifier
    when the `SequenceFile` is instantiated.

    """

    _formats = {
        "fasta": libeasel.sqio.eslSQFILE_FASTA,
        "embl": libeasel.sqio.eslSQFILE_EMBL,
        "genbank": libeasel.sqio.eslSQFILE_GENBANK,
        "ddbj": libeasel.sqio.eslSQFILE_DDBJ,
        "uniprot": libeasel.sqio.eslSQFILE_UNIPROT,
        "ncbi": libeasel.sqio.eslSQFILE_NCBI,
        "daemon": libeasel.sqio.eslSQFILE_DAEMON,
        "hmmpgmd": libeasel.sqio.eslSQFILE_DAEMON,
        "fmindex": libeasel.sqio.eslSQFILE_FMINDEX,
    }


    # --- Class methods ------------------------------------------------------

    @classmethod
    def parse(cls, bytes buffer, str format):
        cdef Sequence seq = TextSequence.__new__(TextSequence)
        seq._sq = libeasel.sq.esl_sq_Create()
        if not seq._sq:
            raise AllocationError("ESL_SQ")
        return cls.parseinto(seq, buffer, format)

    @classmethod
    def parseinto(cls, Sequence seq, bytes buffer, str format):
        assert seq._sq != NULL

        cdef int fmt = libeasel.sqio.eslSQFILE_UNKNOWN
        if format is not None:
            format_ = format.lower()
            if format_ not in cls._formats:
                raise ValueError("Invalid sequence format: {!r}".format(format))
            fmt = cls._formats[format_]

        cdef int status = libeasel.sqio.esl_sqio_Parse(buffer, len(buffer), seq._sq, fmt)
        if status == libeasel.eslEFORMAT:
            raise AllocationError("ESL_SQFILE")
        elif status == libeasel.eslOK:
            return seq
        else:
            raise UnexpectedError(status, "esl_sqio_Parse")


    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self._alphabet = None
        self._sqfp = NULL

    def __init__(self, str file, str format=None):
        cdef int fmt = libeasel.sqio.eslSQFILE_UNKNOWN
        if format is not None:
            format_ = format.lower()
            if format_ not in self._formats:
                raise ValueError("Invalid sequence format: {!r}".format(format))
            fmt = self._formats[format_]

        cdef bytes fspath = os.fsencode(file)
        cdef int status = libeasel.sqio.esl_sqfile_Open(fspath, fmt, NULL, &self._sqfp)
        if status == libeasel.eslENOTFOUND:
            raise FileNotFoundError(2, "No such file or directory: {!r}".format(file))
        elif status == libeasel.eslEMEM:
            raise AllocationError("ESL_SQFILE")
        elif status == libeasel.eslEFORMAT:
            if format is None:
                raise ValueError("Could not determine format of file: {!r}".format(file))
            else:
                raise EOFError("Sequence file appears to be empty: {!r}")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_Checksum")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __dealloc__(self):
        if self._sqfp:
            warnings.warn("unclosed sequence file", ResourceWarning)
            self.close()

    def __iter__(self):
        return self

    def __next__(self):
        seq = self.read()
        if seq is None:
            raise StopIteration()
        return seq


    # --- Read methods -------------------------------------------------------

    cpdef Sequence read(self, bint skip_info=False, bint skip_sequence=False):
        """Read the next sequence from the file.

        Arguments:
            skip_info (`bool`): Pass `True` to disable reading the sequence
                *metadata*, and only read the sequence *letters*. Defaults to
                False`.
            skip_sequence (`bool`): Pass `True` to disable reading the
                sequence *letters*, and only read the sequence *metadata*.
                Defaults to `False`.

        Returns:
            `Sequence`: The next sequence in the file, or `None` if all
            sequences were read from the file.

        Raises:
            `ValueError`: When attempting to read a sequence from a closed
                file, or when the file could not be parsed.

        Hint:
            This method allocates a new sequence, which is not efficient in
            case the sequences are being read within a tight loop. Use
            `SequenceFile.readinto` with an already initialized `Sequence`
            if you can to recycle the internal buffers.

        """
        cdef Sequence seq = TextSequence.__new__(TextSequence)
        seq._sq = libeasel.sq.esl_sq_Create()
        if not seq._sq:
            raise AllocationError("ESL_SQ")
        return self.readinto(seq, skip_info=skip_info, skip_sequence=skip_sequence)

    cpdef Sequence readinto(self, Sequence seq, bint skip_info=False, bint skip_sequence=False):
        """Read the next sequence from the file, using ``seq`` to store data.

        Arguments:
            seq (`~pyhmmer.easel.Sequence`): A sequence object to use to store
                the next entry in the file. If this sequence was used before,
                it must be properly reset (using the `Sequence.clear` method)
                before using it again with `readinto`.
            skip_info (`bool`): Pass `True` to disable reading the sequence
                *metadata*, and only read the sequence *letters*. Defaults to
                False`.
            skip_sequence (`bool`): Pass `True` to disable reading the
                sequence *letters*, and only read the sequence *metadata*.
                Defaults to `False`.

        Returns:
            `~pyhmmer.easel.Sequence`: A reference to ``seq`` that was passed
            as an input, or `None` if no sequences are left in the file.

        Raises:
            `ValueError`: When attempting to read a sequence from a closed
                file, or when the file could not be parsed.

        Example:
            Use `SequenceFile.readinto` to loop over the sequences in a file
            while recycling the same `Sequence` buffer:

            >>> with SequenceFile("vendor/hmmer/testsuite/ecori.fa") as sf:
            ...     seq = TextSequence()
            ...     while sf.readinto(seq) is not None:
            ...         # ... process seq here ... #
            ...         seq.clear()

        """
        assert seq._sq != NULL

        cdef int status
        cdef str function
        cdef ESL_SQFILE* sqfp = self._sqfp

        if sqfp == NULL:
            raise ValueError("I/O operation on closed file.")

        if not skip_info and not skip_sequence:
            function = "esl_sqio_Read"
            with nogil:
                status = libeasel.sqio.esl_sqio_Read(sqfp, seq._sq)
        elif not skip_info:
            function = "esl_sqio_ReadInfo"
            with nogil:
                status = libeasel.sqio.esl_sqio_ReadInfo(sqfp, seq._sq)
        elif not skip_sequence:
            function = "esl_sqio_ReadSequence"
            with nogil:
                status = libeasel.sqio.esl_sqio_ReadSequence(sqfp, seq._sq)
        else:
            raise ValueError("Cannot skip reading both sequence and metadata.")

        if status == libeasel.eslOK:
            return seq
        elif status == libeasel.eslEOF:
            return None
        elif status == libeasel.eslEFORMAT:
            msg = <bytes> libeasel.sqio.esl_sqfile_GetErrorBuf(sqfp)
            raise ValueError("Could not parse file: {}".format(msg.decode()))
        else:
            raise UnexpectedError(status, function)


    # --- Fetch methods ------------------------------------------------------

    cpdef Sequence fetch(self, bytes key, bint skip_info=False, bint skip_sequence=False):
        cdef Sequence seq = TextSequence.__new__(TextSequence)
        seq._sq = libeasel.sq.esl_sq_Create()
        if not seq._sq:
            raise AllocationError("ESL_SQ")
        return self.fetchinto(seq, key, skip_info=skip_info, skip_sequence=skip_sequence)

    cpdef Sequence fetchinto(self, Sequence seq, bytes key, bint skip_info=False, bint skip_sequence=False):
        raise NotImplementedError("TODO SequenceFile.fetchinto")


    # --- Utils --------------------------------------------------------------

    cpdef void close(self):
        libeasel.sqio.esl_sqfile_Close(self._sqfp)
        self._sqfp = NULL

    cpdef Alphabet guess_alphabet(self):
        """Guess the alphabet of an open `SequenceFile`.

        This method tries to guess the alphabet of a sequence file by
        inspecting the first sequence in the file. It returns the alphabet,
        or `None` if the file alphabet cannot be reliably guessed.

        Raises:
            `EOFError`: if the file is empty.
            `OSError`: if a parse error occurred.
            `ValueError`: if this methods is called after the file was closed.

        """

        cdef int ty
        cdef int status
        cdef Alphabet alphabet

        if self._sqfp == NULL:
            raise ValueError("I/O operation on closed file.")

        status = libeasel.sqio.esl_sqfile_GuessAlphabet(self._sqfp, &ty)
        if status == libeasel.eslOK:
            alphabet = Alphabet.__new__(Alphabet)
            alphabet._init_default(ty)
            return alphabet
        elif status == libeasel.eslENOALPHABET:
            return None
        elif status == libeasel.eslENODATA:
            raise EOFError("Sequence file appears to be empty.")
        elif status == libeasel.eslEFORMAT:
            msg = <bytes> libeasel.sqio.esl_sqfile_GetErrorBuf(self._sqfp)
            raise ValueError("Could not parse file: {}".format(msg.decode()))

        return None

    cpdef void set_digital(self, Alphabet alphabet):
        """Set the `SequenceFile` to read in digital mode with ``alphabet``.

        This method can be called even after the first sequences have been
        read; it only affects subsequent sequences in the file.

        """
        if self._sqfp == NULL:
            raise ValueError("I/O operation on closed file.")

        cdef int status = libeasel.sqio.esl_sqfile_SetDigital(self._sqfp, alphabet._abc)
        if status == libeasel.eslOK:
            self._alphabet = alphabet
        else:
            raise UnexpectedError(status, "esl_sqfile_SetDigital")
