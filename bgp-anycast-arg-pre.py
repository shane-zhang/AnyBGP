from _pybgpstream import BGPStream
import pickle as plk
import sys

# Create a new bgpstream instance and a reusable bgprecord instance
stream = BGPStream()

# Consider RIPE RRC 10 only
#stream.add_filter("prefix","8.8.8.0/24")
#stream.add_filter('collector','rrc11')
stream.add_filter('prefix',sys.argv[4])
#stream.add_filter('prefix','199.7.91.0/24')

# Consider this time interval:
# Sat Aug  1 08:20:11 UTC 2015

stream.add_filter('project', 'routeviews')
stream.add_interval_filter(int(sys.argv[1]), int(sys.argv[2]))

# Start the stream
stream.start()

bgp_info = []

# Get next record
rec = stream.get_next_record()
while(rec):
    # Print the record information only if it is not a valid record
#    print (rec.project,"|", rec.collector,"|", rec.type,"|", rec.time,"|", rec.status)
    elem = rec.get_next_elem()
    while(elem):
        # Print record and elem information
#        print (rec.project,"|", rec.collector,"|", rec.type,"|", rec.time,"|" ,rec.status,"|",elem.type,"|", elem.peer_address,"|", elem.peer_asn,"|", elem.fields)
        bgp_info.append([rec.project, rec.collector, rec.type, rec.time, rec.status,elem.type, elem.peer_address, elem.peer_asn, elem.fields])
        elem = rec.get_next_elem()
    rec = stream.get_next_record()
plk.dump(bgp_info,open(sys.argv[3],"wb"))
