import tables as tb

class Event4l( tb.IsDescription ):
    '''
    Defines the n-tuple row for a 4l event.
    For use with PyTables to store the n-tuple in an HDF5 File.
    '''
    channel         = tb.StringCol(16)

    event           = tb.Int32Col()
    lumi            = tb.Int32Col()
    run             = tb.Int32Col()

    pu_weight       = tb.Float64Col()

    mass            = tb.Float64Col()
    pt              = tb.Float64Col()

    z1mass          = tb.Float64Col()
    z1pt            = tb.Float64Col()

    z2mass          = tb.Float64Col()
    z2pt            = tb.Float64Col()

    l1pt            = tb.Float64Col()
    l1eta           = tb.Float64Col()
    l1phi           = tb.Float64Col()

    l2pt            = tb.Float64Col()
    l2eta           = tb.Float64Col()
    l2phi           = tb.Float64Col()

    l3pt            = tb.Float64Col()
    l3eta           = tb.Float64Col()
    l3phi           = tb.Float64Col()

    l4pt            = tb.Float64Col()
    l4eta           = tb.Float64Col()
    l4phi           = tb.Float64Col()

    l1ID            = tb.Int32Col()
    l2ID            = tb.Int32Col()
    l3ID            = tb.Int32Col()
    l4ID            = tb.Int32Col()

    KD              = tb.Float64Col()

    costheta1       = tb.Float64Col()
    costheta2       = tb.Float64Col()
    costhetastar    = tb.Float64Col()
    Phi             = tb.Float64Col()
    Phi1            = tb.Float64Col()

    costheta1_gen   = tb.Float64Col()
    costheta2_gen   = tb.Float64Col()
    costhetastar_gen= tb.Float64Col()
    Phi_gen         = tb.Float64Col()
    Phi1_gen        = tb.Float64Col()
